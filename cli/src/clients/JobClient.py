from clients.AWSClient import AWSClient
from clients.DockerClient import DockerClient
from clients.EnvdClient import EnvdClient
from clients.HttpClient import HttpClient
from utils.console import console
from yaspin import yaspin
import os 
import json

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

        self._inject_access_token()
        self.envd = EnvdClient()
        # self.credentials = self.http_client.get_gcp_credentials()


        # self.docker_client = DockerClient(self.credentials["registry"], self.credentials["username"], self.credentials["password"], debug=False)

       
    def _inject_access_token(self): 
        '''
        Injects the ECR access token into the client's local ~/.docker/config.json for envd to allow image to be pushed
        '''

        '''
        Docker saves authentication settings in the configuration file config.json.

        Linux: ~/.docker/config.json
        Windows: %USERPROFILE%\.docker\config.json
        There are separate sections in the file for different authentication methods:
        
        source = https://cloud.google.com/artifact-registry/docs/docker/authentication
        '''
        # Create the ~/.docker directory if it doesn't exist
        # TODO check windows support, os.path.expanduser should use the correct path 
        # src = https://docs.python.org/3/library/os.path.html
        docker_dir = os.path.expanduser("~/.docker")
        os.makedirs(docker_dir, exist_ok=True)

        # Create the auth dictionary
        injected_config = {} 

        ## Modifying Json fields with Python - https://medium.com/@KaranDahiya2000/modify-json-fields-using-python-1b2d88d16908
        # Write the auth dictionary to ~/.docker/config.json
        self.docker_config_file = os.path.join(docker_dir, 'config.json')
        if os.path.isfile(self.docker_config_file) is True: 
            with open(self.docker_config_file) as existing_config_file:
                injected_config = json.load(existing_config_file)
                
        injected_config["auths"][self.credentials["registry"]]["auth"] = self.credentials['password']

        
        with open(self.docker_config_file, 'w') as f:
            json.dump(injected_config, f, indent=4)

        # TODO logs
        

    def _remove_access_token(self): 
        '''
        Remove previous injected Image Registry access token 
        '''
        injected_config = {}
        with open(self.docker_config_file) as existing_config_file:
            injected_config = json.load(existing_config_file)

        # Remove credentials
        injected_config["auths"].pop(self.credentials["registry"])

        with open(self.docker_config_file, 'w') as f:
            json.dump(injected_config, f, indent=4)


    def start_job(self):
        self.http_client.check_payment_status()

        self.envd.build(self.image_name)
        # TODO check if async is required to ensure that credentials are removed AFTER envd has pushed
        self._remove_access_token()

        # start_build = time.time()

        # self.docker_client.build()

        # end_build = time.time()
        # start_push = time.time()


        # console.print("Image built", style="bold green")
        # console.print("Uploading your code to the cloud", style="bold green")
        # self.docker_client.push(self.image_name)
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
