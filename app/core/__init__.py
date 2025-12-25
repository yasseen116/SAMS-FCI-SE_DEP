"""Core configuration and shared utilities."""
from app.core.database import engine
from app.models.base import Base
from app.models.gallery import Gallery


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized with all tables.")

if __name__ == "__main__":
    init_db()