from prefect_dbt.cloud import DbtCloudCredentials

DbtCloudCredentials(
    api_key="23c576ee64c6975a7ebbfe8389c5b1aa5cca93d3",
    account_id="161290"
).save("dbt-creds")
