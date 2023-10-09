import importlib.resources
import os
import shutil
import tempfile

import typer
import yaml
from python_on_whales import DockerClient as DockerPyClient
from python_on_whales import DockerException
from utils.console import console


class DockerClient:
    def __init__(self, server, username, password, debug=False) -> None:
        self.docker = DockerPyClient()
        self.tag =  "substrate:latest"
        self.docker.login(server=server, username=username, password=password)
        try:
            self.docker.stats()
        except DockerException:
            console.print("Docker engine is not running, please start docker and try again")
            raise typer.Exit(code=1)
        self.debug = debug

    def push(self, image_name):
        self.docker.image.tag(self.tag, image_name)
        self.docker.push(image_name)

    # https://towardsdatascience.com/a-complete-guide-to-building-a-docker-image-serving-a-machine-learning-system-in-production-d8b5b0533bde
    def build(self):
        console.print("Packaging your code", style="bold green")

        # open yaml file and get main location
        with open("substrate.yaml", "rt") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            main_location = yaml_data["main_file_location"]

        # use tempfile to copy requirements.txt to dockerfile directory (traversable)

        with tempfile.TemporaryDirectory() as tempdir:
            # we do two copy because we can then have different docker layers and thus no recreating the requirement layer when we chaneg the code
            shutil.copyfile("./requirements.txt", os.path.join(tempdir, "requirements.txt"))
            shutil.copytree(".", os.path.join(tempdir, "code"))

            dockerfile_traversable = importlib.resources.files("resources").joinpath("Dockerfile")
            with open(dockerfile_traversable, "rt"):
                    # copy dockerfile to tempdir
                    shutil.copyfile(dockerfile_traversable, os.path.join(tempdir, "Dockerfile"))

            cache = False if self.debug else True
            # console.print(f"using cache: {cache}")
            self.docker.build(context_path=tempdir, tags=[self.tag], platforms=["linux/amd64"], build_args={"MAIN_LOCATION": main_location}, cache=cache)
