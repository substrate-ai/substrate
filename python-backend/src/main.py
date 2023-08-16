from functools import lru_cache
import json
import logging
import datetime
import requests

import boto3
from human_id import generate_id
from supabase import create_client
from fastapi import Depends, FastAPI, HTTPException, status

from pydantic import BaseModel
from src.config import Settings
from src.env import config_data
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

class Job(BaseModel):
    jobName : str
    hardware : str 
    token: str
    repoUri: str



@app.post("/start-job")
async def create_item(job: Job):
    token = job.token

    # look at setSession with access_token

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

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    user_id = response.json()['userId']
    

    with open('./resources/aws_hardware_code.json') as f:
        aws_hardware_code = json.load(f)

    if job.hardware not in aws_hardware_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hardware type selected is not supported",
            headers={"WWW-Authenticate": "Basic"},
        )


    instance_type = aws_hardware_code[job.hardware]
    image_name = job.repoUri

    sage = boto3.client('sagemaker', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')

    job_name = generate_id()

    now = datetime.datetime.now()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 

    response = sage.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            'TrainingImage': image_name,
            # todo change input mode
            'TrainingInputMode': 'File',
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
            'MaxRuntimeInSeconds': 60
        }
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


    try:
        supabase_admin.table('job').insert([{
        'job_name': job_name,
        'created_at': iso_time,
        'supabase_id': user_id,
        'hardware': job.hardware,
        'image_name': image_name,
        'status': 'running'
         }]).execute()
    except Exception as e:
        logging.error(e)
        logging.error("job was terminated on aws")

        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in talking to database",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return {
        "jobName": job_name,
    }
    
