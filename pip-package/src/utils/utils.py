import inspect
import os

import requests
import typer
import yaml
from utils.console import console
from utils.env import config_data


def get_user_config():
    try:
        with open(os.path.expanduser('~/.substrate'), 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        console.print("User not logged in", style="bold red")
        raise typer.Exit(code=1)


def get_cli_token():
    return get_user_config()['access_token']

def get_project_config():
    try :
        with open(os.path.join(os.getcwd(), 'substrate.yaml'), 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        error_message = """
        Substrate.yaml not found. \n \
        Potential solutions: \n \
            - The project is not initialized, please run substrate-ai init \n \
            - You are not in the root directory of the project when using the substrate-ai """
        typer.echo(clean_mutliline_string(error_message))
        raise typer.Exit(code=1)

def get_supabase_endpoint():
    return f'{config_data["SUPABASE_URL"]}/functions/v1'

def get_supabase_headers():
    return {"Authorization": f"Bearer {config_data['SUPABASE_ANON_KEY']}"}

def supabase_request(method, path, json):
    endpoint = f'{get_supabase_endpoint()}/{path}'



    # replace with match when moved to python 3.10
    methods = {
        'get': lambda: requests.get(endpoint, headers=get_supabase_headers(), json=json),
        'post': lambda: requests.post(endpoint, headers=get_supabase_headers(), json=json),
        'put': lambda: requests.put(endpoint, headers=get_supabase_headers(), json=json),
        'delete': lambda: requests.delete(endpoint, headers=get_supabase_headers(), json=json),
    }

    response = methods.get(method, lambda: None)()
    if response is None:
        console.print("Failed to make supabase request")
        raise typer.Exit(code=1)

    return response

def get_user_id():
    response = supabase_request('post', 'token/user-id', {"accessToken": get_user_config()['access_token']})
    return response.json()['userId']

def clean_mutliline_string(t):
    return inspect.cleandoc(t)
