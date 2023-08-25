import pkg_resources
import requests
from utils.console import console



def check_update():
    pip_repo_url = "https://pypi.org/pypi/substrate-ai/json"

    response = requests.get(pip_repo_url)

    if response.status_code != 200:
        console.print(f"Failed to check for updates: {response.text}", style="bold red")
        return
    

    current_version = pkg_resources.get_distribution("substrate-ai").version


    latest_version = response.json()["info"]["version"]

    if latest_version != current_version:
        console.print(f"Update available: {latest_version}, current version: {current_version}", style="bold red")
    
    

