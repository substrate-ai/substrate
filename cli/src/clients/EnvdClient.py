import subprocess
import tempfile
import os 
import json
import base64
import uuid

from utils.console import console


class EnvdClient:

    def __init__(self, docker_credentials):
        self.context_name = "remote-buildkit"
        self.server_ip = "buildkit.substrateai.com"
        self.server_port = "8888"
        self.registry_credentials = docker_credentials
        self._inject_access_token()
        self.create_or_use_context()

    def build(self, image_name, push=True):
        console.print("Building image", style="bold green")

        # read requirements.txt
        with open("requirements.txt", "r") as f:
            requirements = f.read()

        # parse requirements.txt to get the list of requirements
        requirements = requirements.replace(" ", "").strip().split("\n")
        console.print(requirements)

        # create the build.envd file with the requirements
        build_context = f"""
        def build():
            install.python_packages(name = {requirements})
        """

        # To do kj why cache is not working
        #.substrate-ai-cache
        # with open(".substrate-ai-cache/build.envd", "w") as f:

        # use tempfile to create a temporary file
        with tempfile.NamedTemporaryFile(mode="w") as f:
            f.write(build_context)
            f.flush()
            # env args to ensure  $DOCKER_HOME is set, this is required by buildctl via envd to retrieve registry credentials
            # https://stackoverflow.com/questions/26643719/python-exporting-environment-variables-in-subprocess-popen
            subprocess.run(["envd", "build", "--output", f"type=image,name={image_name},push={push}"], env={**os.environ,"DOCKER_CONFIG": self.docker_dir})

        self._remove_access_token()

        self._remove_access_token()

        console.print("Image built", style="bold green")

    def create_context(self):
        subprocess.run(["envd", "context", "create", "--name", self.context_name, "--builder", "tcp", "--builder-address", f"{self.server_ip}:{self.server_port}", "--use"])


    def use_context(self):
        subprocess.run(["envd", "context", "use", "--name", self.context_name])

    def create_or_use_context(self):
        # TODO use try catch to check if context exists
        self.create_context()
        self.use_context()


        # try:
        #     self.create_context()
        # except:
        #     self.use_context()

    def _inject_access_token(self): 
        '''
        Injects the ECR access token into the client's local ~/.docker/config.json for envd to allow image to be pushed
        '''

        '''
        Docker saves authentication settings in the configuration file config.json. ̰

        Linux: ~/.docker/config.json
        Windows: %USERPROFILE%\.docker\config.json
        There are separate sections in the file for different authentication methods:
        
        source = https://cloud.google.com/artifact-registry/docs/docker/authentication
        '''
        # Create the ~/.docker directory if it doesn't exist
        # TODO check windows support, os.path.expanduser should use the correct path 
        # src = https://docs.python.org/3/library/os.path.html
        self.docker_dir = os.path.expanduser("~/.docker")
        os.makedirs(self.docker_dir, exist_ok=True)

        # Create the auth dictionary
        injected_config = {} 

        ## Modifying Json fields with Python - https://medium.com/@KaranDahiya2000/modify-json-fields-using-python-1b2d88d16908
        # Write the auth dictionary to ~/.docker/config.json
        self.docker_config_file = os.path.join(self.docker_dir, 'config.json')
        if os.path.isfile(self.docker_config_file) is True: 
            with open(self.docker_config_file) as existing_config_file:
                try:
                    injected_config = json.load(existing_config_file)
                except: 
                    # Existing docker config.json is an invalid json file, hence initialize it as new
                    injected_config = {} 
        
        if not "auths" in injected_config: 
            injected_config["auths"] = {} 
        auth_bytes = f"{self.registry_credentials['username']}:{self.registry_credentials['password']}".encode()
        injected_config["auths"][self.registry_credentials["registry"].split('/')[0]] = {"auth": base64.b64encode(auth_bytes).decode()}

        
        with open(self.docker_config_file, 'w') as f:
            json.dump(injected_config, f, indent=2)
        
        # kj to do logs
        

    def _remove_access_token(self): 
        '''
        Remove previous injected Image Registry access token 
        '''
        injected_config = {}
        with open(self.docker_config_file) as existing_config_file:
            injected_config = json.load(existing_config_file)

        # Remove credentials
        injected_config["auths"].pop(self.registry_credentials["registry"].split('/')[0])

        with open(self.docker_config_file, 'w') as f:
            json.dump(injected_config, f, indent=2)
        
        # kj to do logs


