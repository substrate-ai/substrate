import docker
import boto3
import base64
import os
from env import config_data
import typer
from utils import get_cli_token, get_user_config, get_project_config, get_user_id
from importlib import resources as impresources
import resources
import io
import importlib.resources
import json
from docker.client import DockerClient as DockerPyClient
from human_id import generate_id
import requests

# https://stackoverflow.com/questions/43540254/how-to-stream-the-logs-in-docker-python-api/70059037#70059037

def log_docker_output(generator, task_name: str = 'docker command execution') -> None:
    """
    Log output to console from a generator returned from docker client
    :param Any generator: The generator to log the output of
    :param str task_name: A name to give the task, i.e. 'Build database image', used for logging
    """
    typer.echo(f'Running {task_name}...')
    while True:
        try:
            output = generator.__next__()
            if 'stream' in output:
                output_str = output['stream'].strip('\r\n').strip('\n')
                typer.echo(output_str)
            elif 'status' in output:
                # pass
                output_str = output['status'].strip('\r\n').strip('\n')
                typer.echo("status")
                typer.echo(output_str)
            elif 'error' in output:
                output_str = output['error'].strip('\r\n').strip('\n')
                typer.echo("error")
                typer.echo(output_str)
                raise typer.Exit(code=1)
            else:
                typer.echo(output)
        except StopIteration:
            typer.echo(f'{task_name} complete.')
            break
        except ValueError:
            typer.echo(f'Error parsing output from {task_name}: {output}')

class DockerClient:
    def __init__(self) -> None:
        try:
            self.docker_py_client: DockerPyClient = docker.from_env()
            # self.docker_py_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        except Exception as e:
            # print(e)
            typer.echo(e)
            typer.echo("Please start/install docker to run the the substrate-cli")
            raise typer.Exit(code=1)
        
    def get_tag(self):
        # project_config = get_project_config()
        # project_name = project_config["project_name"]
        # user_id = get_user_id()

        # tag = f"substrate/user_id.{user_id}/project_name.{project_name}:latest"
        tag = f"substrate:latest"
        return tag
    
    # def get_name(self):
    #     project_config = get_project_config()
    #     project_name = project_config["project_name"]
    #     user_id = get_user_id()

    #     name = f"substrate/user_id.{user_id}/project_name.{project_name}"
    #     return name


        
    def build_image(self):

        tag = self.get_tag()

        
        dockerfile_traversable = importlib.resources.files("resources").joinpath("Dockerfile")
        with open(dockerfile_traversable, "rb") as dockerfile:
                image, log_generator = self.docker_py_client.images.build(fileobj=dockerfile, tag=tag, rm=True, forcerm=True)
                log_docker_output(log_generator)
            

        # alternative way to build image
        # dockerfile_path = importlib.resources.as_file(dockerfile_traversable)
        # with importlib.resources.as_file(dockerfile_traversable) as dockerfile_path:
        #     with dockerfile_path.open("rb") as dockerfile:
        #         image, build_log = self.docker_py_client.images.build(fileobj=dockerfile, tag=tag, rm=True, forcerm=True)
        return image
    

        
    
    # https://github.com/AlexIoannides/py-docker-aws-example-project/blob/master/deploy_to_aws.py
    def push(self, repo_uri, username, password, image):
        #todo check credentials
        typer.echo("Pushing image to ECR")

        # registry = '{}/{}'.format(repo_uri.replace('https://', ''), LOCAL_REPOSITORY)
        # registry = f"{repo_uri}/{tag}"
        response = self.docker_py_client.login(username, password, registry=repo_uri)
        if response["Status"] != "Login Succeeded":
            typer.echo("Error logging into ECR, please contact SubstrateAI support")
            raise typer.Exit(code=1)

        image.tag(repo_uri, tag='latest')

        push_log = self.docker_py_client.images.push(repo_uri, tag='latest', stream=True, decode=True)
        log_docker_output(push_log, 'Pushing image to ECR')

        # todo add check that status is pushed at the end, so that we know it worked

class AWS_Client:
    def __init__(self):
        self.docker_py_client = DockerClient()
        access_key_id = config_data["AWS_ACCESS_KEY_ID"]
        secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]
        self.ecr_client = boto3.client('ecr', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
        token = self.ecr_client.get_authorization_token()
        self.username, self.password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        self.registry = token['authorizationData'][0]['proxyEndpoint']    
        typer.echo(f"registry: {self.registry}")

    def push_and_build(self):
        self.docker_py_client.build_and_push(self.registry, self.username, self.password)

        # create a docker repository for the user (should be project repository in the future)
    def get_or_create_user_repo(self):
        repo_name = f"repo.{get_user_id()}"

        # check if repo already exists
        try:
            
            response = self.ecr_client.describe_repositories(repositoryNames=[repo_name])
            typer.echo("repo already exists")
            typer.echo(response)
            repositoryUri = response["repositories"][0]["repositoryUri"]
            return repositoryUri
        except self.ecr_client.exceptions.RepositoryNotFoundException:
            response = self.ecr_client.create_repository(repositoryName=repo_name)
            typer.echo("creating user repo")
            typer.echo(response)
            repositoryUri = response["repository"]["repositoryUri"]
            return repositoryUri
           
class JobClient:
    def __init__(self):
        self.aws_client = AWS_Client()
        self.docker_client = DockerClient()

    def run_container_from_backend(self, repo_uri):
        typer.echo("Running")

        jobName = generate_id()
        hardware = get_project_config()["hardware"]

        auth_token = get_cli_token()
        
        payload = {
            "jobName": jobName,
            "hardware": hardware,
            "token": auth_token,
            "repoUri": repo_uri
        }

        # todo stream the response

        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/launch_job', headers={'Authorization': f'Bearer {auth_token}'}, json=payload)

        if response.status_code != 200:
            typer.echo("Job failed to start")
            return
        
        typer.echo("Job successfully started")

    def stream_logs(self):
        # todo stream logs from aws kinesis
        pass

    def start_job(self):
        typer.echo("Create and push container to ecr aws")
        image = self.docker_client.build_image()
        repo_uri = self.aws_client.get_or_create_user_repo()
        self.docker_client.push(repo_uri, self.aws_client.username, self.aws_client.password, image)
        self.run_container_from_backend()
        self.stream_logs()
        typer.echo("Code successfully uploaded to cloud")






        