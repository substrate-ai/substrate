from google.oauth2 import service_account
from python_on_whales import docker
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request

service_account_key_path = "/Users/baptiste/Git/substrate/envd/buildkit/gcp.json"

request = Request()

credentials = service_account.Credentials.from_service_account_file(
    service_account_key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)
credentials.refresh(request)

if not credentials.valid:
    print("credentials are not valid")
    print("this is weird")
    raise Exception("Failed to use service token")

target_credentials = impersonated_credentials.Credentials(
            credentials, "cli-675@practical-robot-393509.iam.gserviceaccount.com", lifetime=3600, target_scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

target_credentials.refresh(request)

if not target_credentials.valid:
    print("target credentials are not valid")
    print("this is weird")
    raise Exception("Failed to generate access token")

username = "oauth2accesstoken"
password = target_credentials.token
registry = "us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai"

docker.login(registry, username, password)