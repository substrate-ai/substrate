import asyncio

from utils.utils import get_user_config
from utils.utils import supabase_request
from utils.env import config_data
import typer
from utils.utils import get_cli_token, get_project_config
import requests
from utils.console import console
from utils.supabase import supabase_client
import time
from rich.table import Table
import json
import datetime




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
        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/stop-job/{job_name}', json={"accessToken": auth_token})
        if response.status_code != 200:
            console.print(response.text)
            console.print("Job failed to stop")
            raise typer.Exit(code=1)
        
        console.print("Job successfully stopped")





    def get_jobs(self):
        auth_token = get_cli_token()

        @asyncio.coroutine
        async def test_func(loop):
            resp = await supabase_client.functions().invoke("aws/get-jobs", invoke_options={'body':{"accessToken": auth_token}})
            return resp

        loop = asyncio.get_event_loop()
        resp = loop.run_until_complete(test_func(loop))
        loop.close()

        # convert bytes to json
        data = resp.get('data')
        data = data.decode('utf8').replace("'", '"')
        data = json.loads(data)

        # print as rich table
        table = Table(title="Jobs")
        table.add_column("Job Name")
        table.add_column("Hardware")
        table.add_column("Created at")
        table.add_column("Finished at")
        # table.add_column("Runtime")
        table.add_column("Status")



        for job in data:
            # convert 2023-08-24T12:14:03+00:00 into a datetime object
            # format = "%Y-%m-%dT%H:%M:%S.%f%z"
            # console.log(job["created_at"])
            # created_at = datetime.datetime.strptime(job["created_at"], format)

            # finished_at = datetime.datetime.strptime(job["finished_at"], format)

            # todo fix the format of the date
            created_at = job["created_at"]
            finished_at = job["finished_at"]

            # if job["finished_at"] is not None: 
            #     runtime = job["finished_at"] - job["created_at"]
            # else:
            #     runtime = time.time() - job["created_at"]

            # console.print(runtime)
            
            table.add_row(job["job_name"], job["hardware"], created_at, finished_at, job["status"])

        console.print(table)

    

