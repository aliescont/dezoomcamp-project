from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os
import zipfile
os.environ['KAGGLE_USERNAME'] = "aliescont"
os.environ['KAGGLE_KEY'] = "61c51b9c97987be49810bc909802542a"
from kaggle.api.kaggle_api_extended import KaggleApi
import time

@task(log_prints=True, retries = 3)
def download_dataset(kaggle_url:str) -> Path:
    """Download dataset from Kaggle using Kagle API and return the path where dataset is stored"""
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(kaggle_url, path="../../data", unzip = True)  
    cwd = Path.cwd()
    print(cwd)
    prefect_dir = cwd.parent
    main_dir = prefect_dir.parent
    final_path = str(main_dir)+'/data/steam_reviews'
    return final_path

@task()
def filter_df(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues and removing characters that are causing issues during ingestion"""
    #Filtering by reviews in english
    df = df[df['language'] == 'english']
    df = df.reset_index(drop=True)
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def df_chunk_to_csv(df: pd.DataFrame, dataset_file: str, index_file: int) -> Path:
    """Write DataFrame out locally as csv file"""
    df_schema = {
        'app_id' : 'int64',
        'app_name' : 'str',
        'review_id' : 'str',
        'language' : 'str',
        'review' : 'str',
        'recommended' : 'bool',
        'votes_helpful' : 'int64',
        'votes_funny' : 'int64',
        'weighted_vote_score' : 'float',
        'comment_count' : 'float',
        'steam_purchase' : 'bool',
        'received_for_free' : 'bool',
        'written_during_early_access' : 'bool',
        'author.steamid' : 'int64',
        'author.num_games_owned' : 'float',
        'author.num_reviews' : 'float',
        'author.playtime_forever' : 'float',
        'author.playtime_last_two_weeks' : 'float',
        'author.playtime_at_review' : 'float',
        'author.last_played' : 'float'
    }
    #df["timestamp_created"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    #df["timestamp_updated"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    path = Path(f"{dataset_file}_{index_file}.csv") 
    df = df.astype(df_schema)
    df.dropna(inplace=True)
    df.to_csv(path)
    return path

@task()
def write_gcs(path: Path, gcs_path: Path) -> None:
    """Upload local csv file to GCS"""
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=gcs_path)
    return

@flow(log_prints=True)
def ingest_chunk_gcs(df, i, input_path):
    """Ingest each chunk in GCS"""
    #chunk_df = filter_df(df)
    chunk_file_path = df_chunk_to_csv(df, input_path, i)
    print(chunk_file_path)
    output_path = Path(f"data/steam_reviews_{i:02}.csv")
    write_gcs(chunk_file_path, output_path)
    time.sleep(5)
    return

@flow(log_prints=True)
def kaggle_to_gcs() -> None:
    """The main ETL function"""    
    data_path = download_dataset('najzeko/steam-reviews-2021')
    print(data_path)
    source_path = data_path +'.csv'
    print(source_path)
    for i, chunk in enumerate(pd.read_csv(source_path, iterator=True, chunksize=500000, index_col= 0)):
        # if i > n_chunks-1:
        #     break
        ingest_chunk_gcs(chunk, i, data_path)
        time.sleep(5)
        
            
if __name__ == "__main__":

    #n_chunks = 2
    kaggle_to_gcs()