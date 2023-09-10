import requests
from fastapi import HTTPException, status
from resources.env import config_data

supabase_url = config_data["SUPABASE_URL"]
supabase_anon_key = config_data["SUPABASE_ANON_KEY"]


def get_user_id(token: str):

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