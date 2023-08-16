from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import pydantic_settings

# todo fix the env file, not working
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding='utf-8')
    SUPABSE_URL: str = Field("", env='SUPABSE_URL')

