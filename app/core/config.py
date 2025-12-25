"""Application configuration settings."""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Extend with database and auth configuration when implementing."""

    app_name: str = "SAMS SWE Backend"
    api_prefix: str = "/api"
    version: str = "0.1.0"
    allow_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
