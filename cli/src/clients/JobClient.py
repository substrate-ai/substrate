from clients.AWSClient import AWSClient
from clients.DockerClient import DockerClient
from clients.EnvdClient import EnvdClient
from clients.HttpClient import HttpClient
from utils.console import console
from yaspin import yaspin

class JobClient:
    def __init__(self):
        console.print("Initialization...", style="bold green")
        self.http_client = HttpClient()

        # an alternative would be using different tag for each user
        # self.image_name = self.http_client.get_image_name()


        self.aws_client = AWSClient()

        self.credentials = self.aws_client.get_docker_credentials()
        self.image_name = self.aws_client.get_image_name()["imageName"]

        # username, password = self.aws_client.get_ecr_login_password()
        # username, password = self.gcp_client.get_docker_credentials()

        self.envd = EnvdClient(self.credentials)
        # self.credentials = self.http_client.get_gcp_credentials()


        # self.docker_client = DockerClient(self.credentials["registry"], self.credentials["username"], self.credentials["password"], debug=False)

    def start_job(self):
        self.http_client.check_payment_status()

        self.envd.build(self.image_name)

        # start_build = time.time()

        self.docker_client.build()

        # end_build = time.time()
        # start_push = time.time()


        # console.print("Image built", style="bold green")
        # console.print("Uploading your code to the cloud", style="bold green")
        self.docker_client.push(self.image_name)
        # console.print("Code uploaded", style="bold green")

        # end_push = time.time()
        # console.print(f"Time taken to build: seconds {end_build - start_build:.0f}, minutes {(end_build - start_build)/60:.0f}", style="bold yellow")
        # console.print(f"Time taken to push: seconds {end_push - start_push:.0f}, minutes {(end_push - start_push)/60:.0f}", style="bold yellow")
        # console.print(f"Total time: seconds {end_push - start_build:.0f}, minutes {(end_push - start_build)/60:.0f}", style="bold yellow")


        job_name = self.http_client.start_job(self.image_name)
        console.print(f"Job is starting, your job name is {job_name}", style="bold green")

        spinner = yaspin()
        spinner.start()
        self.aws_client.loop_until_job_running(job_name)
        spinner.stop()

        console.print(f"Job {job_name} has started", style="bold green")
        console.print("Streaming your logs", style="bold green")

        try:
            self.aws_client.stream_logs(job_name, True)
        except KeyboardInterrupt:
            console.print("Stopping streaming logs due to keyboard interrupt")
            console.print("Your job is still running in the cloud")

        console.print(f"Job {job_name} terminated", style="bold green")
