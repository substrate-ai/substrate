import time

import boto3
import requests
import typer
from utils.console import console
from utils.env import config_data
from utils.utils import get_cli_token


class AWSClient:
    def __init__(self):
        self.credentials = self.__get_aws_credentials()
        access_key_id = self.credentials["AccessKeyId"]
        secret_access_key = self.credentials["SecretAccessKey"]
        session_token = self.credentials["SessionToken"]
        region_name = config_data["AWS_REGION_NAME"]
        self.logs_client = boto3.client('logs', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name=region_name)
        self.sagemaker_client = boto3.client('sagemaker', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name=region_name)

    def __get_aws_credentials(self):
        # get credentials from backend
        auth_token = get_cli_token()
        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/aws/get-credentials', json={"accessToken": auth_token})
        if response.status_code != 200:
            console.print(response.text)
            console.print("Failed to get cloud credentials")
            raise typer.Exit(code=1)

        credentials = response.json()
        return credentials
    
    def get_docker_credentials(self):
        auth_token = get_cli_token()
        response = requests.get(f'{config_data["PYTHON_BACKEND_URL"]}/aws/docker-credentials', json={"accessToken": auth_token})
        if response.status_code != 200:
            console.print(response.text)
            console.print("Failed to get cloud credentials")
            raise typer.Exit(code=1)

        credentials = response.json()
        return credentials


    def get_image_name(self):
        auth_token = get_cli_token()
        response = requests.get(f'{config_data["PYTHON_BACKEND_URL"]}/aws/image-name', json={"accessToken": auth_token})
        if response.status_code != 200:
            console.print(response.text)
            console.print("Failed to get image name aws")
            raise typer.Exit(code=1)

        image_name = response.json()
        return image_name

    def is_job_running(self, job_name):
        response = self.sagemaker_client.describe_training_job(TrainingJobName=job_name)
        return response['TrainingJobStatus'] in ['InProgress', 'Stopping']
    
    def get_job_status(self, job_name):
        response = self.sagemaker_client.describe_training_job(TrainingJobName=job_name)
        return response['TrainingJobStatus']

    def loop_until_job_running(self, job_name):
        while not self.is_job_running(job_name):
            time.sleep(5)

    def is_job_terminated(self, job_name):
        job_status = self.get_job_status(job_name)
        return job_status in ['Failed', 'Completed', 'Stopped']

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


            job_status = self.get_job_status(job_name)
            
            if job_status in ['Failed', 'Completed', 'Stopped']:
                console.print(f"Job {job_name} has terminated with status {job_status}")
                raise typer.Exit(code=1)


        response = self.logs_client.get_log_events(
            logGroupName='/aws/sagemaker/TrainingJobs',
            logStreamName=log_stream_name,
            startFromHead=True,
        )

        for event in response['events']:
            print(event['message'])

        while 'nextForwardToken' in response:
            time.sleep(3)

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


            job_status = self.get_job_status(job_name)
            
            if job_status in ['Failed', 'Completed', 'Stopped']:
                console.print(f"Job {job_name} has terminated with status {job_status}")
                raise typer.Exit(code=1)


