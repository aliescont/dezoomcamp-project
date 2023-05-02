from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from dbt_cli_flow import trigger_dbt_cli_run

docker_block = DockerContainer.load("steam-docker")

docker_dep = Deployment.build_from_flow(
    flow=trigger_dbt_cli_run,
    name="dbt-core-cli-run",
    infrastructure=docker_block
)

if __name__ == "__main__":
    docker_dep.apply()