## Previous steps

- Create a virtual environment. I used conda.
- Create a new project in GCP.
- Create a IAM Service Account Key
- Create a DBT Cloud account 
- Create a Kaggle account.
- Create a Prefect Cloud account. This step is not mandatory.

### Kaggle
To use Kaggle API, we need to have an account.
Go to Account and create New API Token. 

![Kaggle API](images/kaggle_api.png)
This will download the kaggle.json file. Copy this file in prefect/.kaggle folder

### GCP
- Create a GCP free account
- Create a new project (I've used dezoomcamp-steam)
- Create a Service Account by going to IAM -> Service Accounts -> create a service account
    - To generate a service account, you should include BigQuery Admin, Storage Object Admin, Storage Admin.
    - After creating a service account, in the service account dashboard go to Actions and click manage keys.
    - Click ADD Key -> Create Key -> Select JSON. This will download a json file, save it, you'll need it later.
- Install SDK

### Terraform
- Install Terraform in your OS by following ![these instructions[(https://developer.hashicorp.com/terraform/downloads)
### Docker
To create a deployment in Prefect using docker, I created a Docker image. The steps followed to create the image were 

```shell
docker image build -t aliescont/steam-reviews:dezoomcamp .

docker login 

docker image push aliescont/steam-reviews:dezoomcamp
```
To use that image, the deployment created in Prefect makes reference to that image.

```shell
python3 docker_deploy.py
```
This will create a deployment in the prefect UI

To set the Profile to start agent in Prefect to run the deployment you need to set the PREFECT_API_URL

```shell
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

prefect agent start -q default
```

Finally to run the deployment 

```shell
prefect deployment run kaggle-to-gcs/docker-etl-flow
```

### Prefect

- Install prefect 
```shell
pip install -r requirements.txt
```
- Create Blocks
To create blocks run the python scripts in blocks folder
Please note that to create blocks using scripts, you'll need to provide your service account key and API token for dbt. Don't make this information public.

```shell
#ingest data to GCS
python make_gcp_blocks.py

#create a Docker block to run deployment using a Docker image
python make_docker_blocks.py

#Create a dbt Cloud credentials block to be able to run a dbt job using a Prefect deployment
python make_dbt_creds_blocks.py
```

The deployments can be created using the Prefect UI or by running the corresponding Python scripts in the prefect folder

```shell
#ingest data to GCS
python docker-deploy.py

#load ingested data to GCS into BigQuery
python docker-bq-deploy.py

#run a dbt job
python dbt-cloud.py
```
