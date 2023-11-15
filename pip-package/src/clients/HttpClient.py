import asyncio
import json

import requests
import typer
from rich.table import Table
from utils.console import console
from utils.env import config_data
from utils.supabase import supabase_client
from utils.utils import get_cli_token, get_project_config


class HttpClient:
    def start_job(self, image_name):

        hardware = get_project_config()["hardware"]

        auth_token = get_cli_token()

        payload = {
            "hardware": hardware,
            "token": auth_token,
            "imageName": image_name
        }

        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/aws/start-job', headers={'Authorization': f'Bearer {auth_token}'}, json=payload)

        if response.status_code != 200:
            console.print(response.status_code)
            console.print(response.text)
            console.print("Job failed to start")
            raise typer.Exit(code=1)

        job_name = response.json()["jobName"]

        return job_name

    def stop_job(self, job_name):
        auth_token = get_cli_token()
        response = requests.post(f'{config_data["PYTHON_BACKEND_URL"]}/aws/stop-job/{job_name}', json={"accessToken": auth_token})
        if response.status_code != 200:
            console.print(response.text)
            console.print("Job failed to stop")
            raise typer.Exit(code=1)

        console.print("Job successfully stopped")


    def check_payment_status(self):
        auth_token = get_cli_token()
        header = {"Authorization": f"Bearer {config_data['SUPABASE_ANON_KEY']}"}
        response = requests.get(f'{config_data["SUPABASE_URL"]}/functions/v1/payment/user-status?token={auth_token}', headers=header)

        if response.status_code != 200:
            console.print(response.status_code)
            console.print(response.text)
            console.print("Failed to get payment status")
            raise typer.Exit(code=1)

        payment_status = response.json()["paymentStatus"]

        if payment_status != "active" and payment_status != "admin":
            console.print("To use substrate, you need to add or update your payment method on the SubstrateAI website", style="bold red")
            console.print(f"current payment status: {payment_status}", style="bold red")
            raise typer.Exit(code=1)

    def get_image_name(self):
        json = {"accessToken": get_cli_token()}
        response = requests.get(f'{config_data["PYTHON_BACKEND_URL"]}/gcp/image-name', json=json)
        if response.status_code != 200:
            console.print(response.text)
            console.print("Failed to get image name", style="bold red")
            raise typer.Exit(code=1)

        return response.json()["imageName"]

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

            # TODO parse the format of the date for pretty printing
            created_at = job["created_at"]
            finished_at = job["finished_at"]

            # if job["finished_at"] is not None:
            #     runtime = job["finished_at"] - job["created_at"]
            # else:
            #     runtime = time.time() - job["created_at"]

            # console.print(runtime)

            table.add_row(job["job_name"], job["hardware"], created_at, finished_at, job["status"])

        console.print(table)

    def get_user_id(self):
        auth_token = get_cli_token()
        supabase_url = config_data["SUPABASE_URL"]
        supabase_anon_key = config_data["SUPABASE_ANON_KEY"]

        endpoint = f'{supabase_url}/functions/v1/token/verify-token'
        payload = {'accessToken': auth_token}
        headers = {"Authorization": f"Bearer {supabase_anon_key}"}
        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            console.print(response.text)
            console.print("Failed to get user id")
            raise typer.Exit(code=1)

        return response.json()["userId"]

    def get_gcp_credentials(self):

        json = {"accessToken": get_cli_token()}
        response = requests.get(f'{config_data["PYTHON_BACKEND_URL"]}/gcp/credentials', json=json)
        if response.status_code != 200:
            console.print(response.text)
            console.print("Failed to get gcp credentials")
            raise typer.Exit(code=1)

        return response.json()



