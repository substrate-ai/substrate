from functools import lru_cache
import json
import logging
import datetime
import requests

import boto3
from botocore.exceptions import ClientError
from human_id import generate_id
from supabase import create_client, Client
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from pydantic import BaseModel
from src.config import Settings
from typing_extensions import Annotated

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
print(settings.model_config)

supabase = create_client(settings.SUPABSE_URL, settings.SUPABSE_KEY)


app = FastAPI()

class Job(BaseModel):
    jobName : str
    hardware : str 
    token: str
    repoUri: str

@app.post("/start_job")
async def create_item(job: Job, settings: Annotated[Settings, Depends(get_settings)]):
    token = job.token
    response = requests.post('https://substrate.supabase.co/auth/v1/token/verify', json={'token': token})

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect access token",
            headers={"WWW-Authenticate": "Basic"},
        )

    with open('aws_hardware_code.json') as f:
        aws_hardware_code = json.load(f)


    instance_type = aws_hardware_code[job.hardware]
    image_name = job.repoUri

    sage = boto3.client('sagemaker', region_name='us-east-1')

    job_name = generate_id()


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
            'MaxRuntimeInSeconds': 600
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logging.error(response)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in creating training job",
            headers={"WWW-Authenticate": "Basic"},

        )

        
    now = datetime.datetime.now()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 

    supabase.table('jobs').insert([{
        'job_name': job_name,
        'hardware_code': hardware_code,
        'image_name': image_name,
        'status': 'running',
        'start_time': iso_time
    }]).execute()


    return {
        "response": response,
        "job_name": job_name,
    }
    

