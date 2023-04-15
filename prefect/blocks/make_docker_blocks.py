from prefect.infrastructure.docker import DockerContainer

docker_block = DockerContainer(
    image="aliescont/etl_prefect_steam:dezoomcamp",
    image_pull_policy = "ALWAYS",
    auto_remove=True,
)

docker_block.save("etl-prefect-docker", overwrite=True)