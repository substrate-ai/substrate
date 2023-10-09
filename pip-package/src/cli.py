import typer
from clients.AWSClient import AWSClient
from clients.HttpClient import HttpClient
from clients.JobClient import JobClient
from clients.SetupClient import SetupClient
from utils.check_update import check_update
from utils.console import console
from utils.env import config_data


def init_typer():
    if config_data["PYTHON_BACKEND_URL"] is None:
        console.print("Environment variables are not properly set, contact the developer")
        exit(1)

    check_update()

app = typer.Typer(callback=init_typer, help="Substrate CLI", name="substrate-ai")

@app.command()
def login():
    """
    Login to the substrate platform
    """
    setup_client = SetupClient()
    setup_client.login()

@app.command()
def init():
    """
    Initialize the project folder to be able to run with the substrate platform
    """
    setup_client = SetupClient()
    setup_client.init_folder_creation()

@app.command()
def run():
    """
    Run the project on the substrate platform
    """
    job_client = JobClient()
    job_client.start_job()

@app.command()
def logs(job_name: str):
    """
    Stream the logs of a job
    """
    aws_client = AWSClient()
    aws_client.stream_logs(job_name, False)

@app.command()
def jobs():
    """
    Get all jobs
    """
    # TODO not working
    # TODO add running argument
    http_client = HttpClient()
    http_client.get_jobs()


@app.command()
def stop(job_name: str):
    """
    Stop a job
    """

    aws_client = AWSClient()
    aws_client.stop_job(job_name)


