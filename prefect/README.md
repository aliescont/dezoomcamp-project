## Blocks 
Blocks folder contains script to create blocks needed to run this pipeline. This can be replaced by creating manually in Prefect UI

## Flows
Flows folder contains all scripts needes for flows and deployments in all stages of ELT.  
- dbt_cli_deploy.py -> script to create a Prefect deployment to run dbt models in production.  
- dbt_cli_flow.py -> script for the flow to run a dbt model using prefect_dbt.  
- docker-bq-deploy.py -> script to create a Prefect deployment for flow to ingest data from GCS into BigQuery using Docker.  
- docker-deploy.py -> script to created a Prefect deployment for flow to download data and ingest it into a GCS bucket using Docker.  
- gcs_dim_to_bq -> script to load data used as dimensions from GCS into BigQuery.  
- gcs_to_bq -> script to load all data (facts and dimensions) from GCS into BigQuery.  
- ingest_dimensions_gcs.py -> script to download data to be used as dimension from Kaggle and ingest it in a GCS bucket.  
- ingest_to_gcs.py -> script to ingest raw data into a GCS Bucket, for dimension and facts.

### dbt
prefect-dbt folder contains all files related to dbt project. It's included inside flows because dbt model are created using a Prefect deployment.  

## Docker
Dockerfile contains all steps included in the Docker image to be used for Prefect deployments.  
