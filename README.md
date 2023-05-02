# dezoomcamp-project

This is the final project of [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

## Problem description
Steam is a popular video game distribution platform. According to [Steam Usage and Catalog Stats for 2022](https://backlinko.com/steam-users) in 2022 had 120 million monthly active users, with more than half accessing to the platform at least once a day, which can give us information to analyse the popularity of a video game.   

This project aims to build an end-to-end pipeline that can facilitate data processing to analyse users reviews, answering questions such as
- What is the overall sentiment? most games are recommended or not?
- What is the most active month in which reviews were created?
- For the top 10 games with good reviews, how many bad reviews they have received?
- What are the top free games that have received good reviews?

For future projects, this pipeline can be used as the first step to build:
- A game recommendation system.
- A sentiment analysis app for Steam games.

## Datasets
I've used 2 dataset from Kaggle:

- [This](https://www.kaggle.com/datasets/forgemaster/steam-reviews-dataset) dataset contains users's reviews obtained using Steam API, and can be used as fact.

- [This](https://www.kaggle.com/datasets/tristan581/all-55000-games-on-steam-november-2022) dataset contains general information of 55000 games obtained using Steam API, which can give us better understanding of a game. It can be used as dimensions.

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

## Folder structure

- In [prefect folder](https://github.com/aliescont/dezoomcamp-project/blob/main/prefect/README.md) you'll find all steps for ELT, including blocks and Prefect deployments scripts and dbt models used in Transformation step.

## End-End pipeline

Some of the considerations taken when building this pipeline

- GCS Bucket, dataset and BigQuery tables for sources are created using IaC (Terraform).  
- The datasets used for this project have being extracted from the Steam API at a given time. So, batch processing was selected to ingest this static data into batches to optimize ingestion, but there is no need to use for this use case streaming processing.  
- Data about users' reviews ingested into BigQuery, used as dbt sources, is partitioned by the month in which reviews were created. This was done to optimize query performance when analysing users' reviews in a specific time frame.  

![Diagram](https://github.com/aliescont/dezoomcamp-project/blob/main/images/project_diagram.png)

- Fact table is created using the same partitioned as in source and clustered by "recommended" and "game_name" because these are fields most likely used to analyse users' behaviours in general and for a specific games. This is the lineage created to transform raw data into a data suitable for analysis.

![DBT Lineage](https://github.com/aliescont/dezoomcamp-project/blob/main/images/dbt_steam_lineage.png)
 
## Dashboard
![Dashboard](https://github.com/aliescont/dezoomcamp-project/blob/main/images/dashboard_steam_reviews_agg.png)


