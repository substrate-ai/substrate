from env import config_data
import typer
from utils import get_cli_token, get_project_config
from clients.AWS_Client import AWS_Client
from clients.DockerClient import DockerClient
import requests

class JobClient:
    def __init__(self):
        self.aws_client = AWS_Client()
        access_key_id = config_data["AWS_ACCESS_KEY_ID"]
        secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]
        self.docker_client2 = DockerClient(access_key_id, secret_access_key, 'us-east-1')

    def run_container_from_backend(self, repo_uri):
        typer.echo("Running")

        hardware = get_project_config()["hardware"]

        auth_token = get_cli_token()
        
        payload = {

            "hardware": hardware,
            "token": auth_token,
            "repoUri": repo_uri
        }

        # todo stream the response
        typer.echo("payload")
        typer.echo(payload)

        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/start-job', headers={'Authorization': f'Bearer {auth_token}'}, json=payload)

        if response.status_code != 200:
            typer.echo(response.text)
            typer.echo("Job failed to start")
            raise typer.Exit(code=1)
        
        job_name = response.json()["jobName"]
        
        typer.echo("Job successfully started")

        return job_name


    def start_job(self):
        self.docker_client2.build()
        typer.echo("image built")
        repo_uri = self.aws_client.get_or_create_user_repo()
        typer.echo("repo created")
        self.docker_client2.push(repo_uri)
        typer.echo("image pushed")
        job_name = self.run_container_from_backend(repo_uri)
        typer.echo("job started")
        typer.echo("streaming logs")
        typer.echo(f"Job name {job_name}")

        try:
            self.aws_client.stream_logs(job_name, True)
        except KeyboardInterrupt:
            typer.echo(f"Job name {job_name}")
            typer.echo("Finishing due to keyboard interrupt")
            typer.echo("Your job is still running in the cloud")

        # todo kill stream when job is done

    def stream_logs(self, job_name):
        self.aws_client.stream_logs(job_name, False)