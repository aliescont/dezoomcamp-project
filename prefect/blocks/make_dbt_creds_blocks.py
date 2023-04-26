from prefect_dbt.cloud import DbtCloudCredentials

DbtCloudCredentials(
    api_key="", # add your API key from dbt cloud
    account_id="" # add your account_id from dbt cloud
).save("dbt-creds")
