"""Authentication router."""

from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, get_db
from app.core.config import settings
from app.dto.auth import LoginRequest, Token, UserCreate, UserRead
from app.models.auth import User
from app.services.auth import authenticate_user, create_access_token, create_user, get_user_by_username

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """
    Login endpoint supporting both form-encoded and JSON body.
    """
    content_type = request.headers.get('content-type', '').lower()
    if 'application/json' in content_type:
        body = await request.json()
        try:
            login_request = LoginRequest(**body)
            email = login_request.email
            password = login_request.password
        except Exception as e:
            # Catch validation errors for invalid email format
            if "validation error" in str(e).lower() or "email" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid email format"
                )
            raise
    else:
        if not email or not password:
            raise HTTPException(status_code=400, detail="Invalid login data")

    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "user_id": user.id},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return current_user


