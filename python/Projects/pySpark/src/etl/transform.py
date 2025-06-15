def clean_data(df):
    return df.dropna().dropDuplicates()

def add_column(df):
    return df.withColumn("new_col", df["existing_col"] * 2)
