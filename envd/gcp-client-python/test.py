from google.oauth2 import service_account
# import python on whales
from python_on_whales import docker
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request

service_account_key_path = "/Users/baptiste/Git/substrate/cli/practical-robot-393509-64f9c1ccafe0.json"

credentials = service_account.Credentials.from_service_account_file(
    service_account_key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

if not credentials.valid:
    print("credentials are not valid")
    print("this is weird")

print(credentials.token)


# impersonate service account


target_credentials = impersonated_credentials.Credentials(
            credentials, "cli-675@practical-robot-393509.iam.gserviceaccount.com", lifetime=3600, target_scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

if not target_credentials.valid:
    print("target credentials are not valid")
    print("this is weird")


print(target_credentials.token)


# Create a Request object
request = Request()


# I should be able to refresh credentials (because the credentials have a lifetime of 3600 seconds cf. method argument)
access_token_info = target_credentials.refresh(request)
access_token = access_token_info.token

print(access_token_info.valid)

if not access_token_info:
    raise Exception("Failed to generate access token")


username = "_json_key"


# use probably the access token has a base64 encoded string as password
password = ...
registry = "us-east1-docker.pkg.dev"



docker.login(username, password, registry=registry)
# you know if it works if you have printed login sucessfully