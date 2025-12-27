import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from app.models.base import Base
from app.models.gallery import Gallery
import app.models.staff
import app.models.auth

# manual database initialization script
def init_db():
    """Manually create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
if __name__ == "__main__":
    init_db()