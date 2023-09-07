from functools import lru_cache
import json
import logging
import datetime
from typing import Annotated, Union
import requests

import boto3
from human_id import generate_id
from supabase import create_client
from fastapi import FastAPI, HTTPException, status
from fastapi import FastAPI, Header


from pydantic import BaseModel
from config import Settings
from env import config_data
import logging

@lru_cache()
def get_settings():
    return Settings()

supabase_url = config_data["SUPABASE_URL"]
supabase_anon_key = config_data["SUPABASE_ANON_KEY"]
supabase_admin_key = config_data["SUPABASE_SERVICE_ROLE_KEY"]
access_key_id = config_data["AWS_ACCESS_KEY_ID"]
secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]

supabase_anon = create_client(supabase_url, supabase_anon_key)
supabase_admin = create_client(supabase_url, supabase_admin_key)


app = FastAPI()

class Hardware(BaseModel):
    type: str

class Job(BaseModel):
    hardware : Hardware
    token: str
    repoUri: str

class Token(BaseModel):
    accessToken: str

@app.get("/repository-uri")
def get_ecr_repo_uri(token: Annotated[Union[str, None], Header()] = None):

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect access token",
            headers={"WWW-Authenticate": "Basic"},
        )

    userId = getUser(token)

    ecr_client = boto3.client('ecr', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
    repo_name = f"repo.{userId}"

    # check if repo already exists otherwise create it
    try:
        response = ecr_client.describe_repositories(repositoryNames=[repo_name])
        repositoryUri = response["repositories"][0]["repositoryUri"]
        return {"repositoryUri": repositoryUri}
    except ecr_client.exceptions.RepositoryNotFoundException:
        response = ecr_client.create_repository(repositoryName=repo_name)
        repositoryUri = response["repository"]["repositoryUri"]
        return {"repositoryUri": repositoryUri}

@app.get("/hello")
def hello_world():
    return "hello"

def getUser(token: str):

    # todo should remove first post request and do everything in the second one?
    endpoint = f'{supabase_url}/functions/v1/token/verify-token'
    payload = {'accessToken': token}
    headers = {"Authorization": f"Bearer {supabase_anon_key}"}
    response = requests.post(endpoint, headers=headers, json=payload)


    # todo check for payment status

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect access token",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    endpoint = f'{supabase_url}/functions/v1/token/user-id'
    payload = {'accessToken': token}
    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code != 200 or len(response.json()['userId']) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    
    user_id = response.json()['userId']

    return user_id


@app.post("/stop-job/{job_name}")
async def stop_job(token: Token, job_name: str):
    token = token.accessToken

    user_id = getUser(token)

    # check user of job is same as user of token
    try:
        # todo add .eq('supabase_id', user_id) so match on job_name and user_id
        response = supabase_admin.table('job').select('supabase_id').eq('job_name', job_name).execute()
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in talking to database",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if len(response['data']) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if response['data'][0]['supabase_id'] != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized to stop this job",
            headers={"WWW-Authenticate": "Basic"},
        )

    sage = boto3.client('sagemaker', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
    response = sage.stop_training_job(TrainingJobName=job_name)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in stopping training job",
            headers={"WWW-Authenticate": "Basic"},
        )

    return "Job stopped"

@app.post("/start-job")
async def create_item(job: Job):
    token = job.token

    user_id = getUser(token)

    # call /payment/user_status to check if user has paid
    endpoint = f'{supabase_url}/functions/v1/payment/user-status?id={user_id}'
    headers = {"Authorization": f"Bearer {supabase_anon_key}"}

    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        logging.error("cannot get payment status")
        logging.error(response.status_code)
        logging.error(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="cannot get payment status",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    payment_status = response.json()['paymentStatus']

    if payment_status != 'active' and payment_status != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"user has not paid, current status is {payment_status}",
            
            headers={"WWW-Authenticate": "Basic"},
        )

    with open('./resources/aws_hardware_code.json') as f:
        aws_hardware_code = json.load(f)

    hardwareType = job.hardware.type

    if hardwareType not in aws_hardware_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hardware type selected is not supported",
            headers={"WWW-Authenticate": "Basic"},
        )

    instance_type = aws_hardware_code[hardwareType]

    # check if instance type is valid
    # input_string = "[ml.m6i.xlarge, ml.trn1.32xlarge, ml.p2.xlarge, ml.m5.4xlarge, ml.m4.16xlarge, ml.m6i.12xlarge, ml.p5.48xlarge, ml.m6i.24xlarge, ml.p4d.24xlarge, ml.g5.2xlarge, ml.c5n.xlarge, ml.p3.16xlarge, ml.m5.large, ml.m6i.16xlarge, ml.p2.16xlarge, ml.g5.4xlarge, ml.c4.2xlarge, ml.c5.2xlarge, ml.c6i.32xlarge, ml.c4.4xlarge, ml.c6i.xlarge, ml.g5.8xlarge, ml.c5.4xlarge, ml.c6i.12xlarge, ml.c5n.18xlarge, ml.g4dn.xlarge, ml.c6i.24xlarge, ml.g4dn.12xlarge, ml.c4.8xlarge, ml.g4dn.2xlarge, ml.c6i.2xlarge, ml.c6i.16xlarge, ml.c5.9xlarge, ml.g4dn.4xlarge, ml.c6i.4xlarge, ml.c5.xlarge, ml.g4dn.16xlarge, ml.c4.xlarge, ml.trn1n.32xlarge, ml.g4dn.8xlarge, ml.c6i.8xlarge, ml.g5.xlarge, ml.c5n.2xlarge, ml.g5.12xlarge, ml.g5.24xlarge, ml.c5n.4xlarge, ml.trn1.2xlarge, ml.c5.18xlarge, ml.p3dn.24xlarge, ml.m6i.2xlarge, ml.g5.48xlarge, ml.g5.16xlarge, ml.p3.2xlarge, ml.m6i.4xlarge, ml.m5.xlarge, ml.m4.10xlarge, ml.c5n.9xlarge, ml.m5.12xlarge, ml.m4.xlarge, ml.m5.24xlarge, ml.m4.2xlarge, ml.m6i.8xlarge, ml.m6i.large, ml.p2.8xlarge, ml.m5.2xlarge, ml.m6i.32xlarge, ml.p4de.24xlarge, ml.p3.8xlarge, ml.m4.4xlarge]"


    image_name = job.repoUri

    sage = boto3.client('sagemaker', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')

    job_name = generate_id()

    now = datetime.datetime.now()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 

    training_image_config = {
        'TrainingRepositoryAccessMode': 'Vpc',
        'TrainingRepositoryAuthConfig': {
                'TrainingRepositoryCredentialsProviderArn': 'arn:aws:lambda:us-east-1:038700340820:function:gcp_docker_login'
        }
    }  

    # TODO CONFIG A NEW VPC
    vpc_config = {       
      "SecurityGroupIds": [ "sg-0016597b2395fe358" ],
      "Subnets": [ "subnet-0fa3a4c8eadd61d6f" ]
    }

    
    image_name = "us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai/substrate-ai:latest"
    # todo make a private vpc not accesible online, for the gcp credentials
    # to look at vpc config for external acess (internet) https://docs.aws.amazon.com/sagemaker/latest/dg/docker-containers-adapt-your-own-private-registry.html#docker-containers-adapt-your-own-private-registry-configure

    response = sage.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            'TrainingImage': image_name,
            # todo change input mode
            'TrainingInputMode': 'File',
            'TrainingImageConfig': training_image_config,
        },
        RoleArn='arn:aws:iam::038700340820:role/train',
        OutputDataConfig={
            'S3OutputPath': 's3://substrate-bucket'
        },
        ResourceConfig={
            'InstanceType': instance_type,
            'InstanceCount': 1,
            'VolumeSizeInGB': 1,
        },
        StoppingCondition={
            # todo change max runtime
            'MaxRuntimeInSeconds': 600
        },
        VpcConfig=vpc_config,
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logging.error(response)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in creating training job",
            headers={"WWW-Authenticate": "Basic"},

        )
    else:
        print("job on aws created")

    return 

    try:
        supabase_admin.table('job').insert([{
        'job_name': job_name,
        'created_at': iso_time,
        'supabase_id': user_id,
        'hardware_type': job.hardware.type,
        'aws_instance_type': instance_type,
        'image_name': image_name,
        'status': 'running'
         }]).execute()
    except Exception as e:
        logging.error("error in inserting job into database")
        logging.error(e)
        logging.error("due to error, the job was terminated on aws")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in talking to database",

            headers={"WWW-Authenticate": "Basic"},
        )
    
    return {
        "jobName": job_name,
    }

@app.post("/get-credentials")
async def get_aws_credentials(token: Token):

    # frist get user id from token
    user_id = getUser(token.accessToken)

    # then use sts to assume role
    sts = boto3.client('sts', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
    role_arn = "arn:aws:iam::038700340820:role/CLI_Users"
    role_session_name = f"session.{user_id}"
    response = sts.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logging.error(response)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in getting credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    credentials = response['Credentials']

    return credentials
    

