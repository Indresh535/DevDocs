from pyspark.sql import SparkSession
from src.etl.transform import clean_data

def test_clean_data():
    spark = SparkSession.builder.master("local[*]").appName("Test").getOrCreate()
    df = spark.createDataFrame([(1, "A"), (1, "A"), (None, "B")], ["id", "val"])
    result = clean_data(df)
    assert result.count() == 1
