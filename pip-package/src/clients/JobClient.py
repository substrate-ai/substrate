from clients.AWSClient import AWSClient
from clients.DockerClient import DockerClient
from clients.EnvdClient import EnvdClient
from clients.HttpClient import HttpClient
from clients.JobStateMachine import JobStateMachine
from statemachine import StateMachine, State
from typer import Typer
from utils.console import console
from yaspin import yaspin







class JobClient:
    def __init__(self):
        with console.status("Starting\n", spinner="dots") as status:
            self.http_client = HttpClient()
            self.aws_client = AWSClient()
            self.credentials = self.aws_client.get_docker_credentials()
            self.image_name = self.aws_client.get_image_name()["imageName"]
            self.docker_client = DockerClient(self.credentials["registry"], self.credentials["username"], self.credentials["password"])
            self.http_client.check_payment_status()

        console.print(":heavy_check_mark: [bold green]Started")




    def start_job(self):
        self.docker_client.build()
        self.docker_client.push(self.image_name)
        job_name = self.http_client.start_job(self.image_name)

        with console.status("Job is starting", spinner="dots") as status:
            console.print(f"[blue]Job name is {job_name}")
            self.aws_client.loop_until_job_running(job_name)
        
        console.print(":heavy_check_mark: [bold green]Running your code on the cloud")

        with console.status("Streaming your logs", spinner="dots") as status:
            try:
                self.aws_client.stream_logs(job_name, True)
            except KeyboardInterrupt:
                console.print("Stopping streaming logs due to keyboard interrupt")
                console.print("Your job is still running in the cloud", style="bold red")

        self.aws_client.print_exit_message(job_name)
        
