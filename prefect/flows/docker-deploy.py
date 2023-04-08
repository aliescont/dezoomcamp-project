from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from prefect_etl import etl_web_to_gcs

docker_block = DockerContainer.load("docker-steam")

docker_dep = Deployment.build_from_flow(
    flow=etl_web_to_gcs,
    name="docker-flow",
    infrastructure=docker_block,
)

if __name__ == "__main__":
    docker_dep.apply()