from typing import Optional
from supabase import create_client, Client
import os
import boto3
import docker
import base64
from docker.errors import BuildError
import logging




import typer

app = typer.Typer()

# todo to remove
os.environ['SUPABASE_URL'] = 'https://wahqlmyfzxxydjnhovfg.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndhaHFsbXlmenh4eWRqbmhvdmZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODUzNzgyMDEsImV4cCI6MjAwMDk1NDIwMX0.ZN-WaS4DRO5-2Q7xYYnoVTYSg0eHh9xt2oZQAfFarIE'
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAQSAVYKZKGP6DFEGA'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
os.environ['AWS_DEFAULT_REGION'] = 'eu-east-1'
os.environ['AWS_REPOSITORY_NAME'] = 'substrate'
# os.environ['AWS_REPOSITORY_URL'] = '038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate'

supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

LOCAL_REPOSITORY = 'substrate:latest'

class Config:
    def __init__(self):
        # Docker connection
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            # print(e)
            print("Please start docker")
            print(e)
            exit(1)

        # AWS connection
        self.ecr_client = boto3.client('ecr', region_name='us-east-1')
        token = self.ecr_client.get_authorization_token()
        self.username, self.password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        self.registry = token['authorizationData'][0]['proxyEndpoint']
        self.image_name = '{}/{}'.format(self.registry.replace('https://', ''), LOCAL_REPOSITORY)


config = Config()

# try connect to docker


@app.command()
def login():
    email = typer.prompt("What's your email?")
    email = "collebaptiste@gmail.com"
    data = supabase.auth.sign_in_with_otp({
        "email": email,
        "options": {
            "email_redirect_to": 'https://example.com/welcome'
        }
    })

# https://github.com/AlexIoannides/py-docker-aws-example-project/blob/master/deploy_to_aws.py
# push container to ecr aws
@app.command()
def push():
    typer.echo("Create and push container to ecr aws")
    # push the image to the container registry
    # buildargs={"platform": 'linux/x86_64'}

    # TODO add stream
    try:
        image, build_log = config.docker_client.images.build(path=".", tag=LOCAL_REPOSITORY, platform='linux/x86_64', rm=True)

        for chunk in build_log:
            if 'stream' in chunk:
                for line in chunk['stream'].splitlines():
                   print(line)
    except BuildError as e:
        print("Hey something went wrong with image build!")
        for line in e.build_log:
            if 'stream' in line:
                print(line['stream'].strip())
        raise
    
    print(build_log)

    print(image.id)

    # image is 9gb we need to compress it, multi-stage artcile distroless


    registry = '{}/{}'.format(config.registry.replace('https://', ''), LOCAL_REPOSITORY)

    print(registry)

    print("registry", registry)

    config.docker_client.login(config.username, config.password, registry=registry)

    image.tag(registry, tag='latest')

    print("login done")

    # add stream for push and login and build

    push_log = config.docker_client.images.push(registry, tag='latest')
    print(push_log)

    print("push done")


@app.command()
# run the builded container on aws
def start():
    typer.echo("Running")

    # SageMaker Input Modes

    sage = boto3.client('sagemaker', region_name='us-east-1')
    # TODO to change the name
    response = sage.create_training_job(
        TrainingJobName='todo',
        AlgorithmSpecification={
            'TrainingImage': config.image_name,
            # todo change input mode
            'TrainingInputMode': 'File',
        },
        RoleArn='arn:aws:iam::038700340820:role/train',
        OutputDataConfig={
            'S3OutputPath': 's3://substrate-bucket'
        },
        ResourceConfig={
            'InstanceType': 'ml.m5.large',
            'InstanceCount': 1,
            'VolumeSizeInGB': 1,
        },
        StoppingCondition={
            'MaxRuntimeInSeconds': 600
        }


    )

    print(response)
    
    
    

@app.command()
def hello(name: Optional[str] = None):
    if name:
        typer.echo(f"Hello {name}")
    else:
        typer.echo("Hello World!")


@app.command()
def bye(name: Optional[str] = None):
    if name:
        typer.echo(f"Bye {name}")
    else:
        typer.echo("Goodbye!")


if __name__ == "__main__":
    app()