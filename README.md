# dezoomcamp-project

This is the final projet of [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## Problem description
Steam is a popular video game distribution platform. According to [Steam Usage and Catalog Stats for 2022](https://backlinko.com/steam-users) in 2022 had 120 million monthly active users, with more than half accessing to the platform at least once a day, which can give us information to analyse the popularity of a video game.   

This project aims to build an end-to-end pipeline that can facilitate data processing to analyse users reviews. 

## Datasets
I've used 2 dataset from Kaggle:

- [This](https://www.kaggle.com/datasets/forgemaster/steam-reviews-dataset) dataset contains users's reviews obtained using Steam API, and can be used as fact.

- [This](https://www.kaggle.com/datasets/tristan581/all-55000-games-on-steam-november-2022) dataset contains general information of 55000 games obtained using Steam API, which can give us better understanding of a game. It can be used as dimensions.

As future projects, this pipeline can be used as the first step for a game recommendation system or to build a sentiment analysis for Steam games.

## Technologies used

- Cloud: GCP
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Prefect
- Data Warehouse: BigQuery
- Data visualization: Looker Studio

## Environment setup

- Python 3.9
- Google Cloud SDK
- Terraform
- Prefect
- DBT
- Looker Studio

## End-End pipeline

- GCS Bucket, dataset and BigQuery tables for sources are created using Terraform

![Diagram](https://github.com/aliescont/dezoomcamp-project/blob/main/images/dezoomcamp-steam_diagram.png)

![DBT Lineage](https://github.com/aliescont/dezoomcamp-project/blob/main/images/dbt_steam_lineage.png)
 
## Dashboard
![Dashboard](https://github.com/aliescont/dezoomcamp-project/blob/main/images/dashboard_steam_2.png)


