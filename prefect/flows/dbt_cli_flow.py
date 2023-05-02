
from prefect import flow
from prefect_dbt.cli import DbtCliProfile, DbtCoreOperation

@flow
def trigger_dbt_cli_run() -> str:
    dbt_profile = DbtCliProfile.load("prefect-dbt-cli-block")
    result = DbtCoreOperation(
        commands=["dbt deps", "dbt run --target prod"],
        dbt_cli_profile=dbt_profile,
        project_dir="/opt/prefect/flows/prefect-dbt",
        profiles_dir="/opt/prefect/flows/prefect-dbt"
    ).run()
    return result

if __name__ == "__main__":
    trigger_dbt_cli_run()
