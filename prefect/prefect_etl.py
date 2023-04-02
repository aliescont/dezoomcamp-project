
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os


@task(retries=3)
def fetch(filename: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df_iter = pd.read_csv(filename, iterator=True, chunksize=100000)
    for i, chunk in enumerate(pd.read_csv(filename, iterator=True, chunksize=100000)):
        output_path = Path(f"steam_reviews_{i}.csv")
        chunk.to_csv(output_path, index = False)
    return
    

@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df = df[df['language'] == 'english']
    df['review'] = df['review'].str.replace('\W', ' ', regex=True)
    df['review'] = df['review'].str.replace('\\n', ' ', regex = True)
    #df = df.replace('"', '', regex = True)    
    df["timestamp_created"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    df["timestamp_updated"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    df.rename(columns={"author.steamid": "author_steamid",
                       "author.num_games_owned" : "author_num_games_owned", 
                       'author.num_reviews' : 'author_num_reviews',
                       'author.playtime_forever' : 'author_playtime_forever', 
                       'author.playtime_last_two_weeks' : 'author_playtime_last_two_weeks',
                       'author.playtime_at_review' : 'author_playtime_at_review', 
                       'author.last_played' : 'author_last_played'
                       }, inplace = True)
    #df["author.last_played"] = pd.to_datetime(df["author.last_played"], utc=True, unit='s')
    df = df.reset_index(drop=True)
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def batch_to_parquet(df: pd.DataFrame, dataset_file: str, index_file: int) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"{dataset_file}_{index_file}.csv") 
    df.to_parquet(path)
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
    for i, chunk in enumerate(pd.read_csv(source_path, iterator=True, chunksize=1000000, index_col= 0)):
        chunk = clean(chunk)
        output_path = Path(f"data/steam_reviews_{i}.csv")
        chunk.to_csv(output_path, index = False)
        write_gcs(output_path, output_path)
    return


if __name__ == "__main__":

    etl_web_to_gcs()