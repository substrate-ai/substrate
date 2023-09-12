import base64

import boto3
from fastapi import APIRouter
from internals.utils import get_user_id
from internals.DTOs import Token
from internals.aws_access import access_key_id, secret_access_key


router = APIRouter()

registry = "038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate-ai"


@router.get("/docker-credentials")
def get_repo_credentials(token: Token):

    get_user_id(token.accessToken)

    ecr_client = boto3.client('ecr', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    

    return {"username": username, "password": password, "registry": registry}

@router.get("/image-name")
def get_image_name(token: Token):
    
    user_id = get_user_id(token.accessToken)
    image_name = f"{registry}:{user_id}"
    return {"imageName": image_name}

# @router.get("/repository-uri")
# def get_ecr_repo_uri(token: Annotated[Union[str, None], Header()] = None):

#     if token is None:
#         logging.error("no token provided")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect access token",
#             headers={"WWW-Authenticate": "Basic"},
#         )

#     user_id = get_user_id(token)

#     ecr_client = boto3.client('ecr', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')
#     repo_name = f"repo.{user_id}"

#     # check if repo already exists otherwise create it
#     try:
#         response = ecr_client.describe_repositories(repositoryNames=[repo_name])
#         repository_uri = response["repositories"][0]["repositoryUri"]
#         return {"repositoryUri": repository_uri}
#     except ecr_client.exceptions.RepositoryNotFoundException:
#         response = ecr_client.create_repository(repositoryName=repo_name)
#         repository_uri = response["repository"]["repositoryUri"]
#         return {"repositoryUri": repository_uri}