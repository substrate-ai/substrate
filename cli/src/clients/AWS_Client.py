
import boto3
import base64
from env import config_data
import typer
import time

import sys
import time

import boto3
from env import config_data
import boto3
import time

from utils import get_user_id

class AWS_Client:
    def __init__(self):
        access_key_id = config_data["AWS_ACCESS_KEY_ID"]
        secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]
        self.ecr_client = boto3.client('ecr', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
        self.kinesis_client = boto3.client('kinesis', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
        self.logs_client = boto3.client('logs', aws_access_key_id=config_data["AWS_ACCESS_KEY_ID"], aws_secret_access_key=config_data["AWS_SECRET_ACCESS_KEY"], region_name='us-east-1')

        token = self.ecr_client.get_authorization_token()
        self.username, self.password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        self.registry = token['authorizationData'][0]['proxyEndpoint']    

    # https://stackoverflow.com/questions/47618877/can-i-retrieve-realtime-logs-from-aws-cloudwatch-using-aws-sdk
    def stream_logs(self, job_name):
        typer.echo("streaming logs")

        STREAM_NAME = "sagemaker-job-logs"
        # todo consume logs from kinesis
        try:
            typer.echo(f"Getting connection, iterator and shit...")
            client = self.kinesis_client
            stream = client.describe_stream(StreamName=STREAM_NAME)
            shard_id = stream["StreamDescription"]["Shards"][0]["ShardId"]
            typer.echo(f"Got {shard_id=}")
            iterator = client.get_shard_iterator(
                StreamName=STREAM_NAME,
                ShardId=shard_id,
                ShardIteratorType="LATEST"
            )["ShardIterator"]
            typer.echo(f"Reading data...")
            response = client.get_records(ShardIterator=iterator, Limit=1)

            if not "NextShardIterator" in response:
                typer.echo("Werid not iterator")

            while "NextShardIterator" in response:
                # todo why sleep
                time.sleep(1)
                data = response["Records"]
                if len(data) < 1:
                    print("No data received")
                else:
                    data = data[0]["Data"]
                    print(f"Received {data=}")
                response = client.get_records(ShardIterator=response["NextShardIterator"], Limit=1)
        except KeyboardInterrupt:
            typer.echo("Finishing due to keyboard interrupt")

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
        

    def stream_logs(self, job_name, wait):

        if wait:
            typer.echo("Waiting for logs to be available...")

        while True:
            response = self.logs_client.describe_log_streams(
                logGroupName='/aws/sagemaker/TrainingJobs',
                logStreamNamePrefix=job_name,
                limit=1
            )

            if len(response['logStreams']) > 0:
                log_stream_name = response['logStreams'][0]['logStreamName']
                break

            if not wait:
                print("No log stream found for job: %s" % job_name)
                raise typer.Exit(code=1)
            
            time.sleep(5)


        response = self.logs_client.get_log_events(
            logGroupName='/aws/sagemaker/TrainingJobs',
            logStreamName=log_stream_name,
            startFromHead=True, 
        )

        for event in response['events']:
            print(event['message'])

        while 'nextForwardToken' in response:
            time.sleep(1)
            response = self.logs_client.get_log_events(
                logGroupName='/aws/sagemaker/TrainingJobs',
                logStreamName=log_stream_name,
                startFromHead=True, 
                nextToken=response['nextForwardToken'],
            )

            for event in response['events']:
                print(event['message'])
                