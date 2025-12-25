"""Core configuration and shared utilities."""
from app.core.database import engine, SessionLocal, get_session
from app.core.config import settings
from app.models.base import Base

# Exported symbols
__all__ = ["engine", "SessionLocal", "get_session", "settings"]