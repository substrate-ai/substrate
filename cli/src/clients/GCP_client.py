import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/baptiste/Git/substrate/cli/gcp.json"



from google.cloud import artifactregistry_v1
from utils.console import console
import typer

from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.auth.exceptions import DefaultCredentialsError
import subprocess
import json
from google.auth import impersonated_credentials
# import registry gcp
from google.cloud import container



class GCP_Client:
    def __init__(self) -> None:

        repo = "us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai"

        # container.regis.set_credential_file("/Users/baptiste/Git/substrate/cli/gcp.json")

        # Define the path to your service account JSON key file
        service_account_key_path = "/Users/baptiste/Git/substrate/cli/gcp.json"

# Load the service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_key_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )


        console.print(credentials.valid)

        raise typer.Exit(code=0)

        # self.client = artifactregistry_v1.ArtifactRegistryClient()
        # # self.project = "practical-robot-393509"
        # # self.location = "us-east1"

        # self.client.list_repositories()

        # raise typer.Exit(code=0)
        # self.project = "SubstrateAI"
        # self.location = "us-east1"

        service_account_key_path: str = "/Users/baptiste/Git/substrate/cli/gcp.json"
        target_principal: str = 'cli-675@practical-robot-393509.iam.gserviceaccount.com'

        access_token = self.generate_access_token(service_account_key_path, target_principal)

        console.print(access_token)
        raise typer.Exit(code=1)


    def generate_access_token(service_account_key_path, target_principal, token_lifetime_seconds=3600):

        console.print(service_account_key_path)

        with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as f:
            info = json.load(f)

        cred2 = service_account.Credentials.from_service_account_info(
            info
        )

        console.print(cred2.valid)
        
        # Load the service account key file
        credentials = service_account.Credentials.from_service_account_file(
            '/Users/baptiste/Git/substrate/cli/gcp.json',
            # scopes every service account has
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )


        print(credentials.valid)

        impersonated_credentials.Credentials()

        # Impersonate the service account to get an access token
        target_credentials = impersonated_credentials.Credentials(
            credentials, "cli-675@practical-robot-393509.iam.gserviceaccount.com", lifetime=3600, target_scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        print(target_credentials.valid)

        console.print(target_credentials.token)
        

        # Create a Request object
        request = Request()

        # Obtain the access token using the Request object
        access_token_info = target_credentials.refresh(request)
        access_token = access_token_info.token

        console.print(access_token_info.valid)

        if not access_token_info:
            raise Exception("Failed to generate access token")


        return access_token_info


    def create_access_token(self):
        # Generate an access token
        credentials = service_account.Credentials.from_service_account_file(
            "/Users/baptiste/Git/substrate/cli/gcp.json"
        )

        
        if not credentials.valid:
            credentials.refresh(Request())
        
        access_token = credentials.token

        return access_token

    def get_docker_credentials(self):

        token = self.create_access_token()
        console.print(token)

        # with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as f:
        #         info = json.load(f)

        with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as key_file:
                service_account_key = key_file.read()

        console.print(service_account_key)

        username = "_json_key"


        return username, service_account_key

        # try:

        #     with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as f:
        #         info = json.load(f)
        #     # Generate an access token
        #     credentials = service_account.Credentials.from_service_account_info(
        #         info
        #     )
            
        #     if not credentials.valid:
        #         credentials.refresh(Request())
            
        #     access_token = credentials.token

        #     # Obtain the Docker registry URL for GCR
        #     # registry_url = f"gcr.io/{self.project}/{repo_name}"

        #     # Create the Docker username and password
        #     username = "_json_key"
        #     password = access_token

        #     return username, password

        # except DefaultCredentialsError as e:
        #     typer.echo(f"Error loading credentials: {str(e)}")
        #     raise typer.Exit(code=1)

        

    def create_or_get_repo(self, user_id):
        repo_name = f"repo.{user_id}"

        try:
            repo = self.client.get_repository(name=repo_name)
        except Exception as e:
            # If the repository doesn't exist, create it
            if "Not found" in str(e):
                parent = self.client.location_path(project=self.project, location=self.location)
                repo = {"name": repo_name}
                operation = self.client.create_repository(parent=parent, repository=repo)

                # Wait for the operation to complete
                operation.result()

                return repo_name
            else:
                typer.echo(f"Error: {str(e)}")
                raise typer.Exit(code=1)

        return repo_name


if __name__ == "__main__":
    gcp_client = GCP_Client()
    gcp_client.create_or_get_repo("test")