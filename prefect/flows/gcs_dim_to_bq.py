from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import os, sys
import re
import time

@task(retries=3, log_prints=True)
def extract_from_gcs() -> str:
    """Download steam reviews data from GCS bucket"""
    gcs_path = f"data/steam_games/dimensions/steam_games_v1.csv"
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.get_directory(from_path=gcs_path)
    return gcs_path

@task
def gcs_to_df(file_path: str) -> pd.DataFrame:
    """Convert each csv to a dataframe"""
    df = pd.read_csv(file_path,index_col=0)
    df = df[['appid', 'name', 'short_description', 'developer', 'publisher', 'genre', 'tags','categories', 'languages','release_date']]
    df['release_date'] = pd.to_datetime(df["release_date"])
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
        destination_table="steam_data.steam_games",
        project_id="dezoomcamp-steam-project",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists="append"
    )
    return

@flow()
def etl_gcs_dim_to_bq() -> None:
    """Main flow that extracts data from GCS and creates a subflow to ingest each chunk into a BigQuery table"""
    gcp_path = extract_from_gcs()
    df = gcs_to_df(gcp_path)
    write_bq(df)
    return 


if __name__ == "__main__":
    etl_gcs_dim_to_bq()