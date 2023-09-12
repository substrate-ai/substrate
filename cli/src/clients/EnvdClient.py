import subprocess
import tempfile

from utils.console import console


class EnvdClient:

    def __init__(self):
        self.context_name = "remote-buildkit"
        self.server_ip = "buildkit.substrateai.com"
        self.server_port = "8888"
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

        # TODO why cache is not working
        #.substrate-ai-cache
        # with open(".substrate-ai-cache/build.envd", "w") as f:

        # use tempfile to create a temporary file
        with tempfile.NamedTemporaryFile(mode="w") as f:
            f.write(build_context)
            f.flush()
            subprocess.run(["envd", "build", "--output", f"type=image,name={image_name},push={push}"])

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




