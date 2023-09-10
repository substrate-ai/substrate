import pkg_resources
import requests
from utils.console import console


def check_update():

    package = 'substrate-ai'
    response = requests.get(f'https://pypi.org/pypi/{package}/json')

    if response.status_code != 200:

        console.print(f"Failed to check for updates: {response.status_code}", style="bold red")
        return

    latest_version = response.json()["info"]["version"]
    current_version = pkg_resources.get_distribution("substrate-ai").version

    if latest_version != current_version:
        console.print(f"Update available: {latest_version}, current version: {current_version}", style="bold red")



