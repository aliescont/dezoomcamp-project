from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
import time
import re

@task(log_prints=True, retries = 3)
def download_dataset(kaggle_url:str) -> list:
    """Download dataset from Kaggle using Kagle API and return the path where dataset is stored"""
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(kaggle_url, path="../../data/source", unzip = True)  
    cwd = Path.cwd()
    prefect_dir = cwd.parent
    main_dir = prefect_dir.parent
    final_path = str(main_dir)+'/data/source'
    print(final_path)
    file_path_list = [os.path.join(final_path, file) for file in os.listdir(final_path) if file.endswith('.csv')]
    return file_path_list

@task(log_prints=True, retries = 3)
def df_chunk_to_csv(dataset_file: str) -> list :
    """Split each file in chunk to be ingested in GCS cleaned to avoid data type issues"""
    final_path_list = []
    for i, chunk in enumerate(pd.read_csv(dataset_file, iterator=True, chunksize=400000)):
        output_dataset_file = re.sub('.csv','',dataset_file)
        chunk_path = Path(f"{output_dataset_file}_{i:02}.csv") 
        chunk_df = chunk.reset_index(drop=True)
        #cleaning and converting unix to datetime
        chunk_df['review'] = chunk_df['review'].str.replace('\W', ' ', regex=True)
        chunk_df['review'] = chunk_df['review'].str.replace('\\n', ' ', regex = True)
        chunk_df["timestamp_created"] = pd.to_datetime(chunk_df["unix_timestamp_created"], utc=True, unit='s')
        chunk_df["timestamp_updated"] = pd.to_datetime(chunk_df["unix_timestamp_updated"], utc=True, unit='s')
        chunk_df.drop(columns=['unix_timestamp_created', 'unix_timestamp_updated'], inplace = True)
        print(chunk_path)
        print(chunk_df.head(2))
        print(f"columns: {chunk_df.dtypes}")
        print(f"rows: {len(chunk_df)}")
        chunk_df.to_csv(chunk_path)
        final_path_list.append(chunk_path)
    return final_path_list

@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Upload local csv file to GCS"""
    gcs_path = os.path.join('data/steam_reviews/',os.path.basename(path))
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=gcs_path)
    return

@flow(log_prints=True)
def ingest_chunk_gcs(input_path):
    """Subflow that ingests each chunk in GCS"""
    chunk_file_path_list = df_chunk_to_csv(input_path)
    print(chunk_file_path_list)
    for file_path in chunk_file_path_list:
        write_gcs(file_path)
    return

@flow(log_prints=True)
def kaggle_to_gcs() -> None:
    """The main ETL function"""    
    file_path_list = download_dataset('forgemaster/steam-reviews-dataset')
    for file in file_path_list:
        ingest_chunk_gcs(file)
            
if __name__ == "__main__":

    kaggle_to_gcs()