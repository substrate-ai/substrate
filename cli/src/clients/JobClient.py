from clients.HttpClient import HttpClient
from clients.AWS_Client import AWS_Client
from clients.DockerClient import DockerClient
from utils.console import console
from yaspin import yaspin
import typer


class JobClient:
    def __init__(self):
        console.print("Initialization...", style="bold green")     
        self.aws_client = AWS_Client()
        username, password = self.aws_client.get_ecr_login_password()
        repo = self.aws_client.get_or_create_user_repo()
        self.docker_client = DockerClient(repo, username, password)
        self.http_client = HttpClient()

    def start_job(self):   
        self.http_client.check_payment_status()
        self.docker_client.build()
        console.print("Image built", style="bold green")
        repo_uri = self.aws_client.get_or_create_user_repo()
        console.print("Uploading your code to the cloud", style="bold green")
        self.docker_client.push(repo_uri)
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