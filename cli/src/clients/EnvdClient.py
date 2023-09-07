class EnvdClient:

    def __init__(self):
        self.context_name = "remote-buildkit"
        self.server_ip = "35.211.197.85"
        self.server_port = "8888"
        self.use_context()

    def build(self, image_name, push=True):

        "us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai/substrate-ai"
        f"envd build --output type=image,name={image_name},push={push}"



        
    def create_context(self):
        # TODO seperate string into array

        f"""
        envd context create --name {self.context_name} \
            --builder tcp \
            --builder-address {self.server_ip}:{self.server_ip} \
            --use 
        """
        ...

    def use_context(self):
        f"envd context use --name {self.context_name}"
        ...

    
    
