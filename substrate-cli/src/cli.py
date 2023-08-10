from functools import lru_cache
from typing import Optional
import requests
import os
import typer
from human_id import generate_id
import yaml
from client import AWS_Client
import shutil

app = typer.Typer()

PYTHON_BACKEND_URL: str = os.environ.get("PYTHON_BACKEND_URL")

AWS_ECR_REPOSITORY_NAME = os.environ.get("AWS_ECR_REPOSITORY_NAME")
SUPABSE_URL: str = os.environ.get("SUPABSE_URL")
SUPABSE_KEY: str = os.environ.get("SUPABSE_KEY")


@app.command()
def init():
    typer.echo("Init project with config file and requirements.txt 2")

    # TODO add choice about how to init project
    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'resources/substrate.yaml'), 'substrate.yaml')
    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'resources/requirements.txt'), 'requirements.txt')

    typer.echo("Project successfully initialized")


@app.command()
def login():
    # do while loop
    while True:
        token = typer.prompt("Please enter access token, this can be find in the substrateai.com website")

        response = requests.get(f'{SUPABSE_URL}/functions/v1/token/verify-token', headers={'Authorization': f'Bearer {SUPABSE_KEY}'}, json={"accessToken": token})

        if response.status_code == 200:
            break

        typer.echo("Invalid token, please try again")

    # if exist then load and modify
    if os.path.exists(os.path.expanduser('~/.substrateai')):
        with open(os.path.expanduser('~/.substrateai'), 'r') as f:
            user_config = yaml.load(f)
            user_config['accessToken'] = token
    else:
        user_config = {
            "accessToken": token
        }

    # todo check multipe login
    with open(os.path.expanduser('~/.substrateai'), 'w') as f:
        f.write(yaml.dump(user_config))
    
@lru_cache()
def get_token():
    with open(os.path.expanduser('~/.substrateai'), 'r') as f:
        user_config = yaml.load(f)
        return user_config['accessToken']
    


# https://github.com/AlexIoannides/py-docker-aws-example-project/blob/master/deploy_to_aws.py
# push container to ecr aws
@app.command()
def push():
    typer.echo("Create and push container to ecr aws")

    AWS_Client = AWS_Client()
    AWS_Client.push_and_build()

    typer.echo("Code successfully uploaded to cloud")


@app.command()
# run the builded container on aws
def start():
    typer.echo("Running")

    jobName = generate_id()

    payload = {
        "jobName": jobName,
        "hardwareCode": "g4dn.xlarge",
        "token": get_token(),
        "imageName": "substrate:latest"
    }

    # todo stream the response

    response = requests.post(f'{PYTHON_BACKEND_URL}/launch_job', headers={'Authorization': f'Bearer {get_token()}'}, json=payload)

    if response.status_code != 200:
        typer.echo("Job failed to start")
        return
    
    typer.echo("Job successfully started")
    
    

@app.command()
def hello(name: Optional[str] = None):
    if name:
        typer.echo(f"Hello {name}")
    else:
        typer.echo("Hello World!")


