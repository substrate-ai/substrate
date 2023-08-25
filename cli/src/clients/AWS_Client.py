import boto3
import base64
from utils.env import config_data
import typer
import time
import time
import boto3
from utils.env import config_data
import boto3
import time
from utils.utils import get_user_id
from utils.console import console

class AWS_Client:
    def __init__(self):
        access_key_id = config_data["AWS_ACCESS_KEY_ID"]
        secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]
        self.ecr_client = boto3.client('ecr', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
        self.kinesis_client = boto3.client('kinesis', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
        self.logs_client = boto3.client('logs', aws_access_key_id=config_data["AWS_ACCESS_KEY_ID"], aws_secret_access_key=config_data["AWS_SECRET_ACCESS_KEY"], region_name='us-east-1')
        self.sagemaker_client = boto3.client('sagemaker', aws_access_key_id=config_data["AWS_ACCESS_KEY_ID"], aws_secret_access_key=config_data["AWS_SECRET_ACCESS_KEY"], region_name='us-east-1')

        token = self.ecr_client.get_authorization_token()
        self.username, self.password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        self.registry = token['authorizationData'][0]['proxyEndpoint']    

        # create a docker repository for the user (should be project repository in the future)
    def get_or_create_user_repo(self):
        repo_name = f"repo.{get_user_id()}"

        # check if repo already exists
        try:
            
            response = self.ecr_client.describe_repositories(repositoryNames=[repo_name])
            repositoryUri = response["repositories"][0]["repositoryUri"]
            return repositoryUri
        except self.ecr_client.exceptions.RepositoryNotFoundException:
            response = self.ecr_client.create_repository(repositoryName=repo_name)
            repositoryUri = response["repository"]["repositoryUri"]
            return repositoryUri
        

    def is_job_running(self, job_name):
        response = self.sagemaker_client.describe_training_job(TrainingJobName=job_name)
        return response['TrainingJobStatus'] in ['InProgress', 'Stopping']
    
    def loop_until_job_running(self, job_name):
        while not self.is_job_running(job_name):
            time.sleep(5)

    def is_job_terminated(self, job_name):
        response = self.sagemaker_client.describe_training_job(TrainingJobName=job_name)
        return response['TrainingJobStatus'] in ['Failed', 'Completed', 'Stopped']
    
    def stop_job(self, job_name):
        self.sagemaker_client.stop_training_job(TrainingJobName=job_name)

    def stream_logs(self, job_name, wait):

        # if wait:
        #     console.print("Waiting for logs to be available")

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

            if self.is_job_terminated(job_name):
                break
                

