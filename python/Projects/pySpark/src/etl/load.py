def save_csv(df, path):
    df.write.mode("overwrite").option("header", True).csv(path)

def save_parquet(df, path):
    df.write.mode("overwrite").parquet(path)
