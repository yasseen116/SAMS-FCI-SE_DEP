"""Pydantic schemas for authentication."""

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Schema for reading user data."""
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str
