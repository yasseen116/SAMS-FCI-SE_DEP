"""Database engine/session setup and FastAPI session dependency."""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database URL;
DATABASE_URL = "sqlite:///./app.db"

# Create the SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()