import datetime
import json
import logging
from fastapi import APIRouter, HTTPException, status
from human_id import generate_id
import requests
from internals.DTOs import Job
from internals.utils import get_user_id
from internals.DTOs import Token
import boto3
from internals.supabase_client import supabase_admin, supabase_url, supabase_anon_key
from internals.aws_access import access_key_id, secret_access_key

router = APIRouter()


@router.post("/start-job")
async def create_item(job: Job):
    token = job.token

    user_id = get_user_id(token)

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

    hardware_type = job.hardware.type

    if hardware_type not in aws_hardware_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hardware type selected is not supported",
            headers={"WWW-Authenticate": "Basic"},
        )

    instance_type = aws_hardware_code[hardware_type]

    # check if instance type is valid
    # input_string = "[ml.m6i.xlarge, ml.trn1.32xlarge, ...] 
    # look at the yaml definied in internals

    image_name = job.imageName

    sage = boto3.client('sagemaker', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')

    job_name = generate_id()

    now = datetime.datetime.now()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 

    # training_image_config = {
    #     'TrainingRepositoryAccessMode': 'Vpc',
    #     'TrainingRepositoryAuthConfig': {
    #             'TrainingRepositoryCredentialsProviderArn': 'arn:aws:lambda:us-east-1:038700340820:function:gcp_docker_login'
    #     }
    # }  

    # vpc_config = {       
    #   "SecurityGroupIds": [ "sg-056399f9e5c8f7805" ],

    #   # "subnet-0286b10e9101e4a09", works
    #   # "subnet-0775c57f2d5304587" is not working
    #   # "subnet-0d91098cbc7d78043" works
    #   # Todo why are all not all the subnet working?
      
    #   "Subnets": ["subnet-0286b10e9101e4a09", "subnet-0d91098cbc7d78043"]
    # }

    response = sage.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            'TrainingImage': image_name,
            # todo change input mode
            'TrainingInputMode': 'File',
            # 'TrainingImageConfig': training_image_config,
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
        # VpcConfig=vpc_config,
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

@router.post("/stop-job/{job_name}")
async def stop_job(token: Token, job_name: str):
    token = token.accessToken

    user_id = get_user_id(token)

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