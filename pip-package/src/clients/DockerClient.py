import importlib.resources
import os
import shutil
import subprocess
import tempfile
import typer
import yaml
from python_on_whales import DockerClient as DockerPyClient
from python_on_whales import DockerException
from utils.console import console
from rich.live import Live
from rich.table import Table

class DockerClient:
    def __init__(self, server, username, password, debug=False) -> None:
        self.docker = DockerPyClient()
        self.tag =  "substrate:latest"
        self.docker.login(server=server, username=username, password=password)
        try:
            self.docker.stats()
        except DockerException:
            console.print("Docker engine is not running or not installed, please start docker and try again")
            raise typer.Exit(code=1)
        self.debug = debug

    def push(self, image_name):
        self.docker.image.tag(self.tag, image_name)

        # command = ["docker", "push", image_name]
        # result = subprocess.run(command, capture_output=True, text=True)

        # if result.returncode != 0:
        #     raise RuntimeError(f"Failed to push image '{image_name}': {result.stderr}")
            

        # return result.stdout

        self.docker.push(image_name, quiet=True)




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

            # cache = False if self.debug else True
            cache = False
            # console.print(f"using cache: {cache}")
            logs = self.docker.build(context_path=tempdir, tags=[self.tag], platforms=["linux/amd64"], build_args={"MAIN_LOCATION": main_location}, cache=cache, stream_logs=True)

            # print_dependency = False



            # # Use Live context manager to refresh the terminal output
            # with Live(console=console, refresh_per_second=10) as live:
            #     table = Table(show_header=False, show_edge=False, padding=(0, 1))
            #     table.add_row("Packaging your code...")
            #     live.update(table)
            

            #     for log in logs:
            #         if print_dependency:
            #             table.add_row(f"      {log}", style="purple")
            #             live.update(table)


            #         # todo download base image add a progress bar 038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate-ai:base
            #         if "pip install --no-cache-dir -r /requirements.txt" in log.lower():
            #             try:
            #                 next_line = next(logs)
            #                 if "cached" in next_line.lower():
            #                     print("Dependencies already installed, skipping")
            #                 else:
            #                     # print("Installing dependencies") # TODO today, make this a spinner until dependencies are installed
            #                     print_dependency = True
            #                     table.add_row("Installing dependencies")
            #                     live.update(table)
            #             except StopIteration:
            #                 # Reached the end of the iterator, so there is no next line
            #                 print("Dependencies already installed, skipping")

            #         if "COPY ./code /code" in log.lower():
            #             print_dependency = False
            #             table = Table(show_header=False, show_edge=False, padding=(0, 1))
            #             table.add_row("Dependencies uploaded")
            #             live.update(table)

                
