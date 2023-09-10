from pydantic import BaseModel


class Token(BaseModel):
    accessToken: str  # noqa: N815

class Hardware(BaseModel):
    type: str

class Job(BaseModel):
    hardware : Hardware
    token: str
    imageName: str  # noqa: N815