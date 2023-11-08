from s3fs import S3FileSystem
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')

class FileSystem(S3FileSystem):
    def __init__(self) -> None:
        super().__init__(key=AWS_ACCESS_KEY_ID, secret=AWS_SECRET_ACCESS_KEY, token=AWS_SESSION_TOKEN)