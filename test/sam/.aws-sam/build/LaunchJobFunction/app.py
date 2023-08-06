import json
import logging
import datetime
import requests

# import boto3
from botocore.exceptions import ClientError
from human_id import generate_id
# from supabase import create_client, Client





def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

#     print("hey")
#     aws_hardware_code = {
#     'CPU': 'ml.m5.large',
#     'GPU-T4': 'ml.g4dn.xlarge',
# }

    if not event["body"] or event["body"] == "":
        return {"statusCode": 400, "headers": {}, "body": "Bad Request"}

    body: dict[str, str] = json.loads(event["body"])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }

#     print(get_secret())

#     url: str = ""
#     key: str = ""
#     supabase: Client = create_client(url, key)

#     body = json.loads(event['body'])

#     # call the verify token endpoint

#     token = body['token']
#     response = requests.post('https://substrate.supabase.co/auth/v1/token/verify', json={'token': token})

#     if response.status_code != 200:
#         return {
#             "statusCode": 401,
#             "body": json.dumps({
#                 "message": "unauthorized",
#             }),
#         }
    

    

#     # TODO check the token

#     hardware_code = body['hardware_code']
#     instance_type = aws_hardware_code[hardware_code]
#     image_name = body['image_name']

#     sage = boto3.client('sagemaker', region_name='us-east-1')

#     job_name = generate_id()


#     # TODO to change the name
#     response = sage.create_training_job(
#         TrainingJobName=job_name,
#         AlgorithmSpecification={
#             'TrainingImage': image_name,
#             # todo change input mode
#             'TrainingInputMode': 'File',
#         },
#         RoleArn='arn:aws:iam::038700340820:role/train',
#         OutputDataConfig={
#             'S3OutputPath': 's3://substrate-bucket'
#         },
#         ResourceConfig={
#             'InstanceType': instance_type,
#             'InstanceCount': 1,
#             'VolumeSizeInGB': 1,
#         },
#         StoppingCondition={
#             'MaxRuntimeInSeconds': 600
#         }
#     )

#     if response['ResponseMetadata']['HTTPStatusCode'] != 200:
#         logging.error(response)
#         return {
#             "statusCode": 500,
#             "body": json.dumps({
#                 "response": response,
#             }),
#         }
    
#     now = datetime.datetime.now()
#     iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 

#     # TODO save the job to the database
#     supabase.table('jobs').insert([{
#         'job_name': job_name,
#         'hardware_code': hardware_code,
#         'image_name': image_name,
#         'status': 'running',
#         'start_time': iso_time
#     }]).execute()

#     return {
#         "statusCode": 200,
#         "body": json.dumps({
#             "response": response,
#             "job_name": job_name,
#         }),
#     }




# def get_secret():

#     secret_name = "supabase_secrets"
#     region_name = "us-east-1"

#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )

#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=secret_name
#         )
#     except ClientError as e:
#         # For a list of exceptions thrown, see
#         # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#         raise e

#     # Decrypts secret using the associated KMS key.
#     secret = get_secret_value_response['SecretString']

#     return secret

#     # Your code goes here.
