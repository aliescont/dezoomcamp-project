from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from dbt_core_flow import trigger_dbt_flow

docker_block = DockerContainer.load("steam-docker")

docker_dep = Deployment.build_from_flow(
    flow=trigger_dbt_flow,
    name="dbt-core-run",
    infrastructure=docker_block,
)

if __name__ == "__main__":
    docker_dep.apply()