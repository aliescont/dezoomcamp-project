from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import os, sys
import re
import time

@task(retries=3, log_prints=True)
def extract_from_gcs() -> list:
    """Download steam reviews data from GCS bucket"""
    gcs_path = f"data/steam_reviews/"
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.get_directory(from_path=gcs_path)
    files_list = os.listdir(gcs_path)
    files_path_list = [os.path.join(gcs_path, file) for file in os.listdir(gcs_path)]
    return files_path_list

@task
def gcs_to_df(file_path: str, date_cols: list, schema_dict: dict) -> pd.DataFrame:
    """Convert each csv to a dataframe"""
    df = pd.read_csv(file_path, parse_dates = date_cols, index_col=0)
    df = df.astype(schema_dict)
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery in chunks"""
    gcp_credentials_block = GcpCredentials.load("dezoomcamp-gcp-creds")
    print(f"rows: {len(df)}")
    print(f"columns: {df.dtypes}")
    df.to_gbq(
        destination_table="steam_data.steam_reviews_kaggle",
        project_id="dezoomcamp-steam-project",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists="append",
        chunksize=100000
    )
    return

@flow
def df_chunk_to_bq(file_path: str, date_cols: list, schema_dict: dict)-> None:
    """Flow to ingest a chunk (csv) into a Bigquery table"""
    df_chunk = gcs_to_df(file_path, date_cols, schema_dict)
    write_bq(df_chunk)
    time.sleep(5)
    return

@flow()
def etl_gcs_to_bq(date_cols: list, df_schema: dict) -> None:
    """Main flow that extracts data from GCS and creates a subflow to ingest each chunk into a BigQuery table"""
    gcp_path_list = extract_from_gcs()
    for file in gcp_path_list:
        df_chunk_to_bq(file, date_cols, df_schema)
        time.sleep(5)
    return 


if __name__ == "__main__":
    date_cols = ['timestamp_created','timestamp_updated']
    df_schema = {
        'steamid' : 'int64',
        'appid' : 'int64',
        'voted_up' : 'bool',
        'votes_up' : 'int64',
        'votes_funny' : 'int64',
        'weighted_vote_score' : 'float64',
        'playtime_forever' : 'int64',
        'playtime_at_review' : 'int64',
        'num_games_owned' : 'int64',
        'num_reviews' : 'int64',
        'review' : 'object'
    }
    etl_gcs_to_bq(date_cols, df_schema)