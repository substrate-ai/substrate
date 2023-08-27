import os
import typer
import importlib.resources
import shutil
import tempfile
from python_on_whales import DockerClient as DockerPyClient
from utils.console import console
import yaml

class DockerClient:
    def __init__(self, server, username, password) -> None:
        self.docker = DockerPyClient()
        self.tag =  f"substrate:latest"
        self.docker.login(server=server, username=username, password=password)        
        try:
            self.docker.stats()
        except:
            console.print("Docker engine is not running, please start docker and try again")
            raise typer.Exit(code=1)

    def push(self, repo_uri):
        self.docker.image.tag(self.tag, repo_uri)
        self.docker.push(repo_uri)

    # https://towardsdatascience.com/a-complete-guide-to-building-a-docker-image-serving-a-machine-learning-system-in-production-d8b5b0533bde
    def build(self):
        console.print(f"Packaging your code", style="bold green")

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
            with open(dockerfile_traversable, "rt") as dockerfile:
                    # copy dockerfile to tempdir
                    shutil.copyfile(dockerfile_traversable, os.path.join(tempdir, "Dockerfile"))
            
            image = self.docker.build(context_path=tempdir, tags=[self.tag], platforms=["linux/amd64"], build_args={"MAIN_LOCATION": main_location})