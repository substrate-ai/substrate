from clients.HttpClient import HttpClient
from utils.env import config_data
import typer
from utils.utils import get_cli_token, get_project_config
from clients.AWS_Client import AWS_Client
from clients.DockerClient import DockerClient
import requests
from utils.console import console
from yaspin import yaspin


class JobClient:
    def __init__(self):
        self.aws_client = AWS_Client()
        access_key_id = config_data["AWS_ACCESS_KEY_ID"]
        secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]
        self.docker_client2 = DockerClient(access_key_id, secret_access_key, 'us-east-1')
        self.http_client = HttpClient()

    def start_job(self):
        self.docker_client2.build()
        console.print("Image built", style="bold green")
        repo_uri = self.aws_client.get_or_create_user_repo()
        console.print("Uploading your code to the cloud", style="bold green")
        self.docker_client2.push(repo_uri)
        console.print("Code uploaded", style="bold green")

        job_name = self.http_client.run_container_from_backend(repo_uri)
        console.print(f"Job is starting, your job name is {job_name}", style="bold green")

        spinner = yaspin()
        spinner.start()
        self.aws_client.loop_until_job_running(job_name)
        spinner.stop()

        console.print(f"Job {job_name} has started", style="bold green")
        console.print("Streaming your logs", style="bold green")

        try:
            self.aws_client.stream_logs(job_name, True)
        except KeyboardInterrupt:
            console.print(f"Stopping streaming logs due to keyboard interrupt")
            console.print("Your job is still running in the cloud")

        console.print(f"Job {job_name} terminated", style="bold green")