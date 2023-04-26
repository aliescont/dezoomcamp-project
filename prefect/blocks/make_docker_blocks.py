from prefect.infrastructure.docker import DockerContainer

docker_block = DockerContainer(
    image="aliescont/steam-reviews:dezoomcamp", #update Docker image name as needed
    image_pull_policy = "ALWAYS",
    auto_remove=True,
)

docker_block.save("steam-docker", overwrite=True)