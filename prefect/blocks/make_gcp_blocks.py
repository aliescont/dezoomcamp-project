from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

credentials_block = GcpCredentials(
    service_account_info={
}

  # enter your credentials from the json file inside the {}
)
credentials_block.save("dezoomcamp-gcp-creds", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("dezoomcamp-gcp-creds"),
    bucket="steam_data_lake_dezoomcamp-steam",   
)

bucket_block.save("dezoomcamp-steam-gcs", overwrite=True)
