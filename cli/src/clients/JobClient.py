from clients.GCP_client import GCP_Client
from clients.HttpClient import HttpClient
from clients.AWS_Client import AWS_Client
from clients.DockerClient import DockerClient
from utils.console import console
from yaspin import yaspin
import typer
import time


class JobClient:
    def __init__(self):
        console.print("Initialization...", style="bold green")     
        self.aws_client = AWS_Client()
        self.gcp_client = GCP_Client()
        # username, password = self.aws_client.get_ecr_login_password()
        username, password = self.gcp_client.get_docker_credentials()
        self.http_client = HttpClient()
        # self.repo = self.http_client.get_repo_uri()
        # self.repo = "038700340820.dkr.ecr.us-east-1.amazonaws.com/test"
        # self.repo = self.gcp_client.create_or_get_repo("test")
        self.repo = "us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai"
        console.print(f"Using repository {self.repo}", style="bold green")
        self.docker_client = DockerClient(self.repo, username, password, debug=False)


    def start_job(self):   
        self.http_client.check_payment_status()

        start_build = time.time()

        self.docker_client.build()

        end_build = time.time()
        start_push = time.time()


        console.print("Image built", style="bold green")
        console.print("Uploading your code to the cloud", style="bold green")
        self.docker_client.push(self.repo)
        console.print("Code uploaded", style="bold green")

        end_push = time.time()
        console.print(f"Time taken to build: seconds {end_build - start_build:.0f}, minutes {(end_build - start_build)/60:.0f}", style="bold yellow")
        console.print(f"Time taken to push: seconds {end_push - start_push:.0f}, minutes {(end_push - start_push)/60:.0f}", style="bold yellow")
        console.print(f"Total time: seconds {end_push - start_build:.0f}, minutes {(end_push - start_build)/60:.0f}", style="bold yellow")


        job_name = self.http_client.run_container_from_backend(self.repo)
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