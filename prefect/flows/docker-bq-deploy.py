from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from gcs_to_bq import etl_gcs_to_bq

docker_block = DockerContainer.load("steam-docker")

docker_dep = Deployment.build_from_flow(
    flow=etl_gcs_to_bq,
    name="docker-bq-flow",
    infrastructure=docker_block,
)

if __name__ == "__main__":
    docker_dep.apply()