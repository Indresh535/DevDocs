def read_csv(spark, path):
    return spark.read.option("header", True).csv(path)

def read_parquet(spark, path):
    return spark.read.parquet(path)
