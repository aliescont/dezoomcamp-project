from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from gcs_dim_to_bq import etl_gcs_dim_to_bq
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
def gcs_to_df(file_path: str, date_cols: list) -> pd.DataFrame:
    """Convert each csv to a dataframe"""
    df = pd.read_csv(file_path, parse_dates = date_cols, index_col=0)
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
        project_id="dezoomcamp-steam",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists="append"
    )
    return

@flow
def df_chunk_to_bq(file_path: str, date_cols: list)-> None:
    """Flow to ingest a chunk (csv) into a Bigquery table"""
    df_chunk = gcs_to_df(file_path, date_cols)
    write_bq(df_chunk)
    return

@flow()
def etl_gcs_to_bq() -> None:
    """Main flow that extracts data from GCS and creates a subflow to ingest each chunk into a BigQuery table"""
    date_cols = ['timestamp_created','timestamp_updated']
    etl_gcs_dim_to_bq()
    #ingest steam reviews data
    gcp_path_list = extract_from_gcs()
    for file in gcp_path_list:
        df_chunk_to_bq(file, date_cols)
    return 


if __name__ == "__main__":

    etl_gcs_to_bq()