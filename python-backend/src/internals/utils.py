import logging

import requests
from fastapi import HTTPException, status
from resources.env import config_data
from internals.supabase_client import supabase_admin

supabase_url = config_data["SUPABASE_URL"]
supabase_anon_key = config_data["SUPABASE_ANON_KEY"]

def get_username(id: str):
    # use supabase client to get username
    data = supabase_admin.table('user_data').select('username').eq('id', id).execute()
    
    if data.count == 0 or len(data.data) == 0:
        raise Exception("user not found")
    
    return data.data[0]['username']


def get_user_id(token: str):

    # should remove first post request and do everything in the second one?
    endpoint = f'{supabase_url}/functions/v1/token/verify-token'
    payload = {'accessToken': token}
    headers = {"Authorization": f"Bearer {supabase_anon_key}"}
    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code != 200:
        logging.error("cannot verify token", response.text)
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