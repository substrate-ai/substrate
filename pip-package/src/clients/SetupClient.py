import os
import shutil

import requests
import typer
import yaml
from utils.console import console
from utils.env import config_data
from utils.utils import get_user_config


class SetupClient:

    def __init__(self):
        pass

    def init_folder_creation(self):
        console.print("Init project with config file and requirements.txt")

        project_name = os.path.basename(os.getcwd())

        # load substrate.yaml
        with open(os.path.join(os.path.dirname(__file__), '../resources/substrate.dev.yaml'), 'r') as f:
            substrate_yaml = yaml.safe_load(f)

        substrate_yaml['project_name'] = project_name

        # save substrate.yaml
        with open('substrate.yaml', 'w') as f:
            f.write(yaml.dump(substrate_yaml, sort_keys=False))

        shutil.copyfile(os.path.join(os.path.dirname(__file__), '../resources/requirements.dev.txt'), 'requirements.txt')

        console.print("Project successfully initialized")

    def login(self):
            # do while loop
        while True:
            token = typer.prompt("Please enter access token, this can be find in the substrateai.com website")

            endpoint = f'{config_data["SUPABASE_URL"]}/functions/v1/token/verify-token'
            data = {"accessToken": token}
            headers = {"Authorization": f"Bearer {config_data['SUPABASE_ANON_KEY']}"}

            response = requests.post(endpoint, headers=headers, json=data)

            if response.status_code == 200 and response.json()['verified'] is True:
                break

            console.print("Invalid token, please try again")

        # if exist then load and modify
        if os.path.exists(os.path.expanduser('~/.substrate')):
            user_config = get_user_config()
            user_config['access_token'] = token
        else:
            user_config = {
                "access_token": token
            }

        # save to file
        with open(os.path.expanduser('~/.substrate'), 'w') as f:
            f.write(yaml.dump(user_config))

        console.print("Login successful")

