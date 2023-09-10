
import logging

from fastapi import APIRouter, HTTPException
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from internals.DTOs import Token
from internals.utils import get_user_id

router = APIRouter()

@router.get("/gcp/image-name")
def get_image_name(token: Token):
    
    user_id = get_user_id(token.accessToken)
    repo_url = "us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai"

    image_name = f"{repo_url}/{user_id}:latest"
    return {"imageName": image_name}



@router.get("/gcp/credentials")
def get_gcp_credentials(token: Token):

    # check user is valid
    get_user_id(token.accessToken)


    service_account_key_path = "./resources/gcp.json"

    request = Request()

    credentials = service_account.Credentials.from_service_account_file(
        service_account_key_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    credentials.refresh(request)

    if not credentials.valid:
        logging.error("credentials are not valid")
        raise HTTPException(status_code=500, detail="Failed to use service token")
    

    target_credentials = impersonated_credentials.Credentials(
                credentials, "cli-675@practical-robot-393509.iam.gserviceaccount.com", lifetime=3600, target_scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )

    target_credentials.refresh(request)

    if not target_credentials.valid:
        logging.error("target credentials are not valid")
        raise HTTPException(status_code=500, detail="Failed to generate access token")

    username = "oauth2accesstoken"
    password = target_credentials.token
    registry = "us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai"
    return {"username": username, "password": password, "registry": registry}






