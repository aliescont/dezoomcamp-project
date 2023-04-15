from prefect import flow

from prefect_dbt.cloud import DbtCloudCredentials
from prefect_dbt.cloud.jobs import trigger_dbt_cloud_job_run


@flow
def trigger_dbt_cloud_job_run_flow(dbt_job_id:int):
    credentials = DbtCloudCredentials.load("dbt-creds")
    trigger_dbt_cloud_job_run(dbt_cloud_credentials=credentials, job_id=dbt_job_id)

if __name__=="__main__":
    job_id = 264715
    trigger_dbt_cloud_job_run_flow(job_id)
