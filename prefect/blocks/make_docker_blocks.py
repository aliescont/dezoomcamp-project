from prefect.infrastructure.docker import DockerContainer

docker_block = DockerContainer(
    image="aliescont/prefect:steam",
    image_pull_policy = "ALWAYS",
    auto_remove=True,

)

docker_block.save("steam-test", overwrite=True)