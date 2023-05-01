from prefect import flow
from prefect_dbt.cli.commands import DbtCoreOperation

@flow
def trigger_dbt_flow() -> str:
    result = DbtCoreOperation(
        commands=["dbt deps", "dbt run --target prod"],
        project_dir="/opt/prefect/flows/prefect-dbt",
        profiles_dir="/opt/prefect/flows/prefect-dbt"
    ).run()
    return result

if __name__ == "__main__":
    trigger_dbt_flow()
