from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import IntegerType, FloatType

def clean_nulls(df):
    """Replaces IMDb's specific '\\N' string with actual Spark Nulls."""
    for column in df.columns:
        df = df.withColumn(column, when(col(column) == '\\N', None).otherwise(col(column)))
    return df

def main():
    spark = SparkSession.builder \
        .appName("IMDb_Lakehouse_ETL") \
        .master("spark://spark-master:7077") \
        .getOrCreate()
    
    # 1. Extract
    titles_df = spark.read.option("header", "true").option("sep", "\t").csv("./data/raw/title.basics.tsv")
    ratings_df = spark.read.option("header", "true").option("sep", "\t").csv("./data/raw/title.ratings.tsv")
    
    # 2. Transform 
    titles_df = clean_nulls(titles_df)
    ratings_df = clean_nulls(ratings_df)
    
    titles_df = titles_df.withColumn("startYear", col("startYear").cast(IntegerType())) \
                         .withColumn("runtimeMinutes", col("runtimeMinutes").cast(IntegerType()))
    ratings_df = ratings_df.withColumn("averageRating", col("averageRating").cast(FloatType())) \
                           .withColumn("numVotes", col("numVotes").cast(IntegerType()))

    titles_df = titles_df.filter(col("startYear").isNotNull())

    # 3. Join & Load to Lake
    enriched_df = titles_df.join(ratings_df, on="tconst", how="left")
    output_path = "./data/lake/imdb_enriched.parquet"
    
    # Partition by startYear for efficient time-series OLAP queries
    enriched_df.write \
        .mode("overwrite") \
        .partitionBy("startYear") \
        .option("compression", "snappy") \
        .parquet(output_path)
        
    spark.stop()

if __name__ == "__main__":
    main()
