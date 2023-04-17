from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import os, sys
import re

@task(retries=3, log_prints=True)
def extract_from_gcs() -> list:
    """Download steam reviews data from GCS"""
    gcs_path = f"data/"
    gcs_block = GcsBucket.load("dezoomcamp-steam-gcs")
    gcs_block.get_directory(from_path=gcs_path)
    files_list = os.listdir(gcs_path)
    files_path_list = [os.path.join(gcs_path, file) for file in os.listdir(gcs_path)]
    return files_path_list

@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""
    gcp_credentials_block = GcpCredentials.load("dezoomcamp-gcp-creds")
    print(f"rows: {len(df)}")
    print(f"columns: {df.dtypes}")
    #df["timestamp_created"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    #df["timestamp_updated"] = pd.to_datetime(df["timestamp_updated"], utc=True, unit='s')
    df.to_gbq(
        destination_table="steam_data.steam_reviews_data_cleaned",
        project_id="dezoomcamp-steam-project",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        if_exists="append",
        chunksize=100_000
    )

@task()
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues and removing characters that are causing issues during ingestion"""
    #df = df[df['language'] == 'english']
    #df["review"] = df["review"].map(lambda text: re.sub(r"\W", ' ', text))

    # df['review'] = df['review'].str.replace('\W', ' ', regex=True)
    # df['review'] = df['review'].str.replace('\\n', ' ', regex = True)
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
    df = df.reset_index(drop=True)
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task
def gcs_to_df(file_path: str, date_cols: list, schema_dict: dict) -> pd.DataFrame:
    df = pd.read_csv(file_path, index_col=0, parse_dates=date_cols)
    df.dropna(inplace=True)
    df = df.astype(schema_dict)
    print(df.head())
    print(df.dtypes)
    return df

@flow
def df_chunk_to_bq(file_path: str, date_cols: list, schema_dict: dict)-> None:
    df_chunk = gcs_to_df(file_path, date_cols, schema_dict)
    df_chunk_cleaned = clean(df_chunk)
    write_bq(df_chunk_cleaned)
    return

@flow()
def etl_gcs_to_bq():
    gcp_path_list = extract_from_gcs()
    print(gcp_path_list)
    date_cols = ['timestamp_created','timestamp_updated']
    df_schema = {
        'app_id' : 'int64',
        'app_name' : 'str',
        'review_id' : 'int64',
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
    #gcp_path_list = ['/home/aliciescont/Documents/Github/dezoomcamp-project/prefect/data/steam_reviews_00.csv']
    for file in gcp_path_list:
        df_chunk_to_bq(file, date_cols, df_schema)
    return 



if __name__ == "__main__":

    etl_gcs_to_bq()