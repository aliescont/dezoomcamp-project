from prefect_gcp.credentials import GcpCredentials
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile

gcp_credentials_block = GcpCredentials.load("dezoomcamp-gcp-creds")

target_configs = BigQueryTargetConfigs(
    schema="steam_prod",  # update with your production dataset name
    credentials=gcp_credentials_block,
)
target_configs.save("prefect-dbt-target")

dbt_cli_profile = DbtCliProfile(
    name="dbt_steam", #update profile name in dbt_project.yml as needed
    target="prod", #update target name, prod is used for production environemnt
    target_configs=target_configs,
)
dbt_cli_profile.save("prefect-dbt-cli-block")
