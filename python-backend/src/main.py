from fastapi import FastAPI
from routers.aws import aws

app = FastAPI()

app.include_router(aws.router)