"""FastAPI application entry point and router registration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine
# FIX 1: Import Base directly from database.py, not just .core
from .core.database import Base
from .routers import announcements, auth, dashboard, gallery, staff

# FIX 2: Explicitly import the models so SQLAlchemy knows about them
import app.models.staff 

app = FastAPI(title=settings.app_name, version=settings.version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(announcements.router, prefix=settings.api_prefix)
app.include_router(gallery.router, prefix=settings.api_prefix)
app.include_router(staff.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(dashboard.router, prefix=settings.api_prefix)

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    # Because we imported app.models.staff above, this will now create the table
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized")

@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}