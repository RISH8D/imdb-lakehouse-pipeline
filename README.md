# IMDb Lakehouse to OLAP Pipeline

This repository demonstrates a modern, end-to-end data pipeline built for analytical workloads using **PySpark** for data transformation and **ClickHouse** as the OLAP serving layer.

## Architecture & Performance Choices

Teleparty's viewership requirements mimic heavy event-driven workloads where analysts need sub-second aggregations.

* **Automated Data Ingestion:** Instead of requiring manual downloads, I integrated the Kaggle API (`scripts/download_data.py`). This guarantees reproducibility. Anyone cloning this repo can execute the pipeline end-to-end without leaving the terminal, adhering to standard CI/CD and automated pipeline principles.
* **The Lake (Spark):** I used PySpark to clean `\N` null types and cast schema types, writing the output as Parquet files partitioned by `startYear`. Partitioning by year avoids the "small files problem" while keeping the data highly scannable for chronological queries.
* **The OLAP (ClickHouse):** I chose ClickHouse over running raw Spark SQL for the presentation layer. ClickHouse's column-oriented `MergeTree` engine is explicitly designed for high-concurrency, low-latency analytics. By mapping a primary index to `(titleType, startYear, averageRating)`, analysts can retrieve aggregations exponentially faster than a Spark DAG can spin up and scan memory.
* **Idempotency (Truncate-and-Load):** The ClickHouse ingestion script uses `TRUNCATE TABLE` before loading. This guarantees that the pipeline is perfectly idempotent and can be re-run indefinitely without duplicating data or destroying the underlying DDL schema and permissions (which `DROP TABLE` would do).
* **Zero-Dependency Containerization:** The entire Python orchestrator, PySpark environment, and Java dependency are containerized in a custom Dockerfile. A user cloning this repository does *not* need to install Python, Java, or Virtual Environments on their host machine. The entire architecture spins up via a single `docker-compose` command.
* **Resource Efficiency:** Rather than deploying permanent, RAM-heavy Spark Master and Worker containers, the orchestrator triggers PySpark using `.master("local[*]")`. This spins up an ephemeral Spark cluster that temporarily maxes out the physical CPU cores to crunch the data, and then immediately releases the RAM back to the system when the job finishes.

## AI Usage Note

I used ChatGPT to generate the boilerplate PySpark syntax and the Docker Compose skeleton, which saved a lot of typing. However, I manually designed the partitioning strategy, the ClickHouse indexing, and the benchmarking script. You can check `PROMPTS.md` for the exact iterative prompts I used.

## Execution Guide

1. Clone this repository and ensure `kaggle.json` is in the root directory.
2. Spin up the infrastructure and run the automated pipeline orchestrator in one command:
   ```bash
   docker compose up --build
   ```
