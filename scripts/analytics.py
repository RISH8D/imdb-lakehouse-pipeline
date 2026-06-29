import time
import clickhouse_connect
from pyspark.sql import SparkSession

QUERY_SPARK = """
    SELECT startYear, titleType, AVG(averageRating) as avg_rating 
    FROM imdb 
    WHERE numVotes > 50000 
    GROUP BY startYear, titleType 
    ORDER BY startYear DESC 
    LIMIT 10
"""

QUERY_CH = """
    SELECT startYear, titleType, AVG(averageRating) as avg_rating 
    FROM imdb_analytics 
    WHERE numVotes > 50000 
    GROUP BY startYear, titleType 
    ORDER BY startYear DESC 
    LIMIT 10
"""

def benchmark_spark():
    spark = SparkSession.builder.master("local[*]").appName("Benchmark").getOrCreate()
    df = spark.read.parquet("./data/lake/imdb_enriched.parquet")
    df.createOrReplaceTempView("imdb")
    
    start_time = time.time()
    spark.sql(QUERY_SPARK).collect()
    end_time = time.time()
    
    spark.stop()
    return end_time - start_time

def benchmark_clickhouse():
    client = clickhouse_connect.get_client(host='localhost', port=8123)
    
    start_time = time.time()
    client.query(QUERY_CH)
    end_time = time.time()
    
    return end_time - start_time

if __name__ == "__main__":
    print("Running benchmarks...")
    spark_time = benchmark_spark()
    ch_time = benchmark_clickhouse()
    
    print(f"\n--- Results ---")
    print(f"PySpark Query Time:    {spark_time:.4f} seconds")
    print(f"ClickHouse Query Time: {ch_time:.4f} seconds")
    print(f"ClickHouse is {spark_time/ch_time:.1f}x faster for this workload.")
