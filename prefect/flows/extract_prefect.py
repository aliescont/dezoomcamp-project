
import os
import zipfile
import pandas as pd
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset(kaggle_url:str) -> Path:
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(kaggle_url, path="../../data/source", unzip = True)    
    return

if __name__ == "__main__":
    url = 'https://www.kaggle.com/datasets/najzeko/steam-reviews-2021/download?datasetVersionNumber=1'
    download_dataset('muhammedzidan/car-prices-market')