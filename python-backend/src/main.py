from fastapi import FastAPI
from routers import aws, gcp

app = FastAPI()

app.include_router(gcp.router)
app.include_router(aws.router)