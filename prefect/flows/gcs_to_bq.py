from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3, log_prints=True)
def extract_from_gcs(chunk_number: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/steam_reviews_{chunk_number}.csv"
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.get_directory(from_path=gcs_path)
    return Path(f"{gcs_path}")


@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""
    gcp_credentials_block = GcpCredentials.load("dezoomcamp-creds")
    print(f"rows: {len(df)}")
    print(f"columns: {df.dtypes}")
    df.to_gbq(
        destination_table="steam_data.steam_reviews_data_2021",
        project_id="dezoomcamp-steam-project",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists="append",
    )

@flow(log_prints=True)
def etl_gcs_to_bq(chunk_number: int):
    """Main ETL flow to load data into Big Query in batches"""
    path = extract_from_gcs(chunk_number)
    print(path)
    df = pd.read_csv(path, index_col=0)
    print(df.head())
    df["timestamp_created"] = pd.to_datetime(df["timestamp_updated"])
    df["timestamp_updated"] = pd.to_datetime(df["timestamp_updated"])
    write_bq(df)


if __name__ == "__main__":
    n_chunks = 2
    for i in range(n_chunks): 
        etl_gcs_to_bq(i)