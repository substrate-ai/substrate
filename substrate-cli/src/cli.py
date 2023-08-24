import typer
from env import config_data
from clients.JobClient import JobClient
from clients.SetupClient import SetupClient

def init_typer():
    if config_data["PYTHON_BACKEND_URL"] is None:
        typer.echo("Environment variables are not properly set, contact the developer")
        exit(1)

app = typer.Typer(callback=init_typer)

@app.command()
def init():
    setup_client = SetupClient()
    setup_client.init_folder_creation()

@app.command()
def login():
    setup_client = SetupClient()
    setup_client.login()

@app.command()
def run():
    job_client = JobClient()
    job_client.start_job()    

@app.command()
def logs(job_name: str):
    job_client = JobClient()
    job_client.stream_logs(job_name)

def get_jobs():
    # TODO
    pass

def stop():
    # TODO
    pass


