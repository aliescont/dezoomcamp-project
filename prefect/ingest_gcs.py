

from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os


@task(retries=3)
def fetch(filename: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df_iter = pd.read_csv(filename, iterator=True, chunksize=100000)

    df = next(df_iter)

    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["timestamp_created"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    df["timestamp_updated"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def batch_to_parquet(df: pd.DataFrame, dataset_file: str, index_file: int) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"{dataset_file}_{index_file}.parquet") 
    df.to_parquet(path)
    return path


@task()
def write_gcs(path: Path, gcs_path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=gcs_path)
    return


@flow()
def etl_web_to_gcs(index_file) -> None:
    """The main ETL function"""
    
    source_path = "/home/aliciescont/Documents/Github/dezoomcamp-project/data/steam_reviews.csv"
    output_path = Path(f"data/steam_reviews_{index_file}.parquet")
  
    df = fetch(source_path)
    df_clean = clean(df)
    path = batch_to_parquet(df_clean, source_path, index_file)
    write_gcs(path, output_path)


if __name__ == "__main__":
    index_file = 0
    while True:
        index_file += 1
        try:   
            etl_web_to_gcs(index_file)

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break 