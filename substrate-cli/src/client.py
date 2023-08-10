import docker
import boto3
import base64
import os

AWS_ECR_REPOSITORY_NAME = os.environ.get("AWS_ECR_REPOSITORY_NAME")


class DockerClient:
    def __init__(self) -> None:
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            # print(e)
            print("Please start docker")
            print(e)
            exit(1)

    def build_image(self):
        image, build_log = self.docker_client.images.build(path=".", tag=f"{AWS_ECR_REPOSITORY_NAME}:latest", platform='linux/x86_64', rm=True)
        return image

    def push_to_ecr(self, aws_registry, aws_username, aws_password, image):
        print("aws_registry", aws_registry)
        print("AWS_ECR_REPOSITORY_NAME", AWS_ECR_REPOSITORY_NAME)
        # push to ecr
        parsed_registry = '{}/{}'.format(aws_registry.replace('https://', ''), f"{AWS_ECR_REPOSITORY_NAME}:latest")
        print("parsed_registry", parsed_registry)

        self.docker_client.login(aws_username, aws_password, registry=parsed_registry)

        image.tag(parsed_registry, tag='latest')
        image_name = '{}/{}'.format(aws_registry.replace('https://', ''), f"{AWS_ECR_REPOSITORY_NAME}:latest")
        print("image_name", image_name)

        self.docker_client.images.push(image_name, auth_config={'username': aws_username, 'password': aws_password})
        print("Pushed to ECR")

    def build_and_push(self, aws_registry, aws_username, aws_password):
        image = self.build_image()
        self.push_to_ecr(aws_registry, aws_username, aws_password, image)

class AWS_Client:
    def __init__(self):

        self.docker_client = DockerClient()
        self.ecr_client = boto3.client('ecr', region_name='us-east-1')
        token = self.ecr_client.get_authorization_token()
        self.username, self.password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        self.registry = token['authorizationData'][0]['proxyEndpoint']

    

    def push_and_build(self):
        self.docker_client.build_and_push(self.registry, self.username, self.password)

   