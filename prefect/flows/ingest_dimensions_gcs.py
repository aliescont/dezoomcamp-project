from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os
os.environ['KAGGLE_USERNAME'] = "aliescont"
os.environ['KAGGLE_KEY'] = "61c51b9c97987be49810bc909802542a"
from kaggle.api.kaggle_api_extended import KaggleApi
import time


@task(log_prints=True, retries = 3)
def download_dataset(kaggle_url:str) -> str:
    """Download dataset to be used as dimensions from Kaggle using Kagle API and return the path where dataset is stored"""
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(kaggle_url, path="../../data/source/dimensions/", unzip = True)  
    cwd = Path.cwd()
    prefect_dir = cwd.parent
    main_dir = prefect_dir.parent
    final_path = str(main_dir)+'/data/source/dimensions/'
    print(final_path)
    return final_path


@task(log_prints=True, retries = 3)
def csv_to_df(filename: str) -> str :
    full_path = Path(filename + 'steam_games.json')
    df = pd.read_json(full_path, orient='index', encoding='utf-8')
    #df = df[['appid', 'genre', 'languages']]
    #df = df[['appid', 'name', 'short_description', 'developer', 'publisher', 'genre', 'tags', 'type','categories', 'languages']]
    #df.drop(columns=['platforms', 'tags', 'short_description', 'categories', 'name'], inplace=True)
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    final_path = filename + 'steam_games_v1.csv'
    df.to_csv(final_path)
    return final_path

@task(log_prints=True)
def write_gcs(path: Path) -> None:
    """Upload local csv file to GCS"""
    gcs_path = os.path.join('data/steam_games/dimensions',os.path.basename(path))
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=gcs_path)
    return


@flow(log_prints=True)
def ingest_dim_to_gcs() -> None:
    """The main ETL function"""    
    file_path = download_dataset('tristan581/all-55000-games-on-steam-november-2022')
    dim_path = csv_to_df(file_path)
    write_gcs(dim_path)
    return

if __name__ == "__main__":

    ingest_dim_to_gcs()
