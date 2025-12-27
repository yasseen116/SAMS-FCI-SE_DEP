"""Application configuration settings."""
import secrets
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Extend with database and auth configuration when implementing."""

    app_name: str = "SAMS SWE Backend"
    api_prefix: str = "/api"
    version: str = "0.1.0"
    allow_origins: List[str] = ["*"]

    # JWT settings
    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


settings = Settings()
