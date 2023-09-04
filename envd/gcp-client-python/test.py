from google.oauth2 import service_account

service_account_key_path = "/Users/baptiste/Git/substrate/cli/practical-robot-393509-64f9c1ccafe0.json"

credentials = service_account.Credentials.from_service_account_file(
    service_account_key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

print(credentials.valid)

# debug to find out why credentials are not valid


# cannot login in into google clients (python client)

# issue with docker push and login