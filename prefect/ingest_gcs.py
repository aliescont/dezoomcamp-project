

from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os



@task(retries=3)
def fetch(filename: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df_iter = pd.read_csv(filename, iterator=True, chunksize=10000, index_col=0)

    return df_iter

@task(log_prints=True)
def clean(df_iter: pd.DataFrame) -> pd.DataFrame:
    df = next(df_iter)
    print(df.head())
    df = df[df['language'] == 'english']
    print('filtered by language')
    df = df.replace('\\n', '', regex = True)
    print('removing newlines')
    df = df.reset_index(drop=True)
    print('start cleaning dates')
    df["timestamp_created"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    df["timestamp_updated"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')

    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def batch_to_parquet(df: pd.DataFrame, dataset_file: str, index_file: int) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"{dataset_file}_{index_file}.csv") 
    df.to_csv(path)
    return path


@task()
def write_gcs(path: Path, gcs_path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=gcs_path)
    return


@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    
    source_path = "/home/aliciescont/Documents/Github/dezoomcamp-project/data/steam_reviews.csv"
    index_file = 0
    df_iter = df_iter = pd.read_csv(source_path, iterator=True, chunksize=10000, index_col=0)
    while True:
        try:
            index_file += 1
            output_path = Path(f"data/steam_reviews_{index_file}.csv")
            df_next = clean(df_iter)
            print(df_next.head())
            path = batch_to_parquet(df_next, source_path, index_file)
            write_gcs(path, output_path)
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break 

if __name__ == "__main__":
    index_file = 0
    
    etl_web_to_gcs()
