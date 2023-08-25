from utils.utils import get_user_config
from utils.utils import supabase_request
from utils.env import config_data
import typer
from utils.utils import get_cli_token, get_project_config
import requests
from utils.console import console

class HttpClient:
    def run_container_from_backend(self, repo_uri):

        hardware = get_project_config()["hardware"]

        auth_token = get_cli_token()
        
        payload = {

            "hardware": hardware,
            "token": auth_token,
            "repoUri": repo_uri
        }

        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/start-job', headers={'Authorization': f'Bearer {auth_token}'}, json=payload)

        if response.status_code != 200:
            console.print(response.text)
            console.print("Job failed to start")
            raise typer.Exit(code=1)
        
        job_name = response.json()["jobName"]
        
        console.print("Job successfully started")

        return job_name
    
    def stop_job(self, job_name):
        auth_token = get_cli_token()
        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/stop-job/{job_name}', headers={'Authorization': f'Bearer {auth_token}'})
        if response.status_code != 200:
            console.print(response.text)
            console.print("Job failed to stop")
            raise typer.Exit(code=1)
        
        console.print("Job successfully stopped")

    def get_jobs(self):
        auth_token = get_cli_token()
        response = supabase_request('get', '/aws/get-jobs', json={"accessToken": auth_token})
        if response.status_code != 200:
            console.print(response.status_code)
            console.print(response.text)
            console.print("Failed to get jobs")
            raise typer.Exit(code=1)
        
        console.print("Jobs successfully retrieved")
        return response.json()