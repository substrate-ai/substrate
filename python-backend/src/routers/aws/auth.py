import logging
from fastapi import APIRouter, HTTPException, status
from internals.utils import get_user_id
from internals.DTOs import Token
import boto3
from internals.aws_access import access_key_id, secret_access_key


router = APIRouter()

def _get_aws_credentials(token: str):
    # frist get user id from token
    user_id = get_user_id(token)

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


@router.post("/get-credentials")
async def get_aws_credentials(token: Token):
    return _get_aws_credentials(token.accessToken)
    
    

