import boto3
import json
import logging

from fastapi import Body, APIRouter
from internals.utils import get_username, get_user_id
from internals.aws_access import access_key_id, secret_access_key, account_id

router = APIRouter()

def create_s3_access_policy(bucket_name, username):
    """
    Create an IAM policy that allows access to the specified S3 bucket.
    """
    iam = boto3.client('iam')
    policy_name = f"S3AccessPolicyForUser_{username}"
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
            }
        ]
    }
    iam.create_policy(
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy_document)
    )
    return policy_name

def create_role_for_user(username, policy_name):
    """
    Create an IAM role for a user and attach the specified policy.
    """
    iam = boto3.client('iam')
    role_name = f"RoleForUser_{username}"
    role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                # OPTION 1
                # "Effect": "Allow",
                # "Principal": {
                #     "Service": "sts.amazonaws.com"  # Update the Principal to STS
                    
                # },
                # "Action": "sts:AssumeRole",
                # "Condition": {
                #     "StringEquals": {
                #         "sts:ExternalId": username  # You can use an external ID if needed
                #     }
                # }

                # OPTION 2
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{account_id}:user/fastapi"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(role_policy)
    )
    iam.attach_role_policy(
        PolicyArn=f"arn:aws:iam::{account_id}:policy/{policy_name}",
        RoleName=role_name
    )
    return role_name

def create_s3_bucket(bucket_name):
    """
    Create an S3 bucket.
    """
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)

def assume_user_role(username, role_name):
    """
    Assume the user-specific role using STS.
    """
    sts = boto3.client('sts', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
    role_session_name = f"session.{username}"
    response = sts.assume_role(RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}", RoleSessionName=role_session_name)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logging.error(response)
        raise Exception("Error in getting credentials")

    return response['Credentials']


def _user_created_s3_hook(username):
    bucket_name = username
    create_s3_bucket(bucket_name)
    policy_name = create_s3_access_policy(bucket_name, username)
    create_role_for_user(username, policy_name)
    return "ok"

def _get_user_s3_credentials(username):
    role_name = f"RoleForUser_{username}"
    print(role_name)
    credentials = assume_user_role(username, role_name)
    return credentials

@router.post("/get-user-s3-credentials")
def get_user_s3_credentials_from_token(payload = Body(None)):
    token = payload["accessToken"]
    user_id = get_user_id(token)
    username = get_username(user_id)

    return _get_user_s3_credentials(username)


@router.post("/create-user-bucket")
def user_created_s3_hook(payload = Body(None)):
    username = payload["record"]["username"]
    return _user_created_s3_hook(username)

