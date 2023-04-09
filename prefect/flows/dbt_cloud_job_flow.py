from prefect import flow

from prefect_dbt.cloud import DbtCloudCredentials
from prefect_dbt.cloud.jobs import trigger_dbt_cloud_job_run


@flow
def trigger_dbt_cloud_job_run_flow():
    credentials = DbtCloudCredentials.load("dbt-creds")
    trigger_dbt_cloud_job_run(dbt_cloud_credentials=credentials, job_id=264715)

trigger_dbt_cloud_job_run_flow()
