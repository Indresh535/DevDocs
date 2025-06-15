from config.spark_config import get_spark_session
from src.etl.extract import read_csv
from src.etl.transform import clean_data, add_column
from src.etl.load import save_parquet

def main():
    spark = get_spark_session("ETLJob")
    df = read_csv(spark, "data/raw/input.csv")
    df_clean = clean_data(df)
    df_transformed = add_column(df_clean)
    save_parquet(df_transformed, "data/processed/output.parquet")

if __name__ == "__main__":
    main()
