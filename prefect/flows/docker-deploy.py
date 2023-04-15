from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from ingest_to_gcs import kaggle_to_gcs

docker_block = DockerContainer.load("etl-prefect-docker")

docker_dep = Deployment.build_from_flow(
    flow=kaggle_to_gcs,
    name="docker-etl-flow",
    infrastructure=docker_block,
)

if __name__ == "__main__":
    docker_dep.apply()