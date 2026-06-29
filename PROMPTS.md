# AI Prompt Log

This document logs the step-by-step prompts used to generate the boilerplate code for this pipeline, demonstrating the architectural direction provided to the LLM.

**Prompt 1:** "Generate a docker-compose.yml file with a Spark master, Spark worker, and a ClickHouse database." 
*Result:* AI generated the basic infra, but forgot to map the shared volumes so Spark and ClickHouse could see the same files.

**Prompt 2:** "Update that docker-compose file. Add a shared volume `./data:/data` to all three containers so ClickHouse can read the Parquet files Spark writes."

**Prompt 3:** "Write the PySpark boilerplate to read the IMDb TSV files. Note: The dataset uses `\N` for nulls. Make sure you handle this before casting the `startYear` to an Integer."

**Prompt 4:** "Give me the ClickHouse DDL for the joined dataset using MergeTree. Actually, make sure you add an `ORDER BY` clause using `titleType` and `startYear` since that's how we will query the analytics."

**Prompt 5:** "Write a ClickHouse DDL script using `clickhouse_connect`. The engine must be `MergeTree`. I want the `ORDER BY` clause optimized specifically for an analytics workload that frequently groups by `titleType` and sorts by `averageRating`. Include the ingestion command to read Snappy-compressed Parquet files directly from a local volume."
