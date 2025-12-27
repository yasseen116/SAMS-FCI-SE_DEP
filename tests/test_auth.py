"""Comprehensive authentication system tests."""

import pytest
from fastapi import status

from app.models.auth import User
from app.services.auth import create_user, hash_password
from app.dto.auth import UserCreate


class TestRegistration:
    """Test user registration functionality."""

    def test_register_new_user_success(self, client, test_user_data):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json={
            "username": test_user_data["username"],
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
        assert "id" in data
        assert "password" not in data

    def test_register_duplicate_email(self, client, test_user_data, db_session):
        """Test registration with duplicate email."""
        # Create first user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"])
        )
        db_session.add(user)
        db_session.commit()

        # Try to register with same email
        response = client.post("/api/auth/register", json={
            "username": "anotheruser",
            "email": test_user_data["email"],
            "password": "AnotherPass123!"
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]

    def test_register_duplicate_username(self, client, test_user_data, db_session):
        """Test registration with duplicate username."""
        # Create first user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"])
        )
        db_session.add(user)
        db_session.commit()

        # Try to register with same username
        response = client.post("/api/auth/register", json={
            "username": test_user_data["username"],
            "email": "newemail@example.com",
            "password": "AnotherPass123!"
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "TestPassword123!"
        })

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLogin:
    """Test user login functionality with email."""

    def test_login_with_email_json_success(self, client, test_user_data, db_session):
        """Test successful login with email using JSON."""
        # Create user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"]),
            role="user"
        )
        db_session.add(user)
        db_session.commit()

        # Login with email
        response = client.post("/api/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_with_email_form_success(self, client, test_user_data, db_session):
        """Test successful login with email using form data."""
        # Create user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"]),
            role="user"
        )
        db_session.add(user)
        db_session.commit()

        # Login with email using form
        response = client.post("/api/auth/login", data={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_email(self, client, test_user_data, db_session):
        """Test login with non-existent email."""
        # Create user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"])
        )
        db_session.add(user)
        db_session.commit()

        # Try login with wrong email
        response = client.post("/api/auth/login", json={
            "email": "wrong@example.com",
            "password": test_user_data["password"]
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_wrong_password(self, client, test_user_data, db_session):
        """Test login with wrong password."""
        # Create user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"])
        )
        db_session.add(user)
        db_session.commit()

        # Try login with wrong password
        response = client.post("/api/auth/login", json={
            "email": test_user_data["email"],
            "password": "WrongPassword123!"
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_inactive_user(self, client, test_user_data, db_session):
        """Test login with inactive user account."""
        # Create inactive user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"]),
            is_active=False
        )
        db_session.add(user)
        db_session.commit()

        # Try to login
        response = client.post("/api/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })

        # Login succeeds but using the token should fail
        if response.status_code == status.HTTP_200_OK:
            token = response.json()["access_token"]
            me_response = client.get("/api/auth/me", headers={
                "Authorization": f"Bearer {token}"
            })
            assert me_response.status_code == status.HTTP_403_FORBIDDEN


class TestTokenAuthentication:
    """Test JWT token-based authentication."""

    def test_get_current_user_success(self, client, test_user_data, db_session):
        """Test getting current user info with valid token."""
        # Create user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"]),
            role="user"
        )
        db_session.add(user)
        db_session.commit()

        # Login to get token
        login_response = client.post("/api/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]

        # Get current user info
        response = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
        assert data["role"] == "user"

    def test_get_current_user_no_token(self, client):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token."""
        response = client.get("/api/auth/me", headers={
            "Authorization": "Bearer invalid_token_here"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_malformed_header(self, client):
        """Test accessing protected endpoint with malformed auth header."""
        response = client.get("/api/auth/me", headers={
            "Authorization": "InvalidFormat token"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAdminAuthorization:
    """Test admin role authorization."""

    def test_admin_access_success(self, client, test_admin_data, db_session):
        """Test admin user can access admin-protected endpoints."""
        # Create admin user
        admin = User(
            username=test_admin_data["username"],
            email=test_admin_data["email"],
            hashed_password=hash_password(test_admin_data["password"]),
            role="admin"
        )
        db_session.add(admin)
        db_session.commit()

        # Login as admin
        login_response = client.post("/api/auth/login", json={
            "email": test_admin_data["email"],
            "password": test_admin_data["password"]
        })
        token = login_response.json()["access_token"]

        # Verify user info shows admin role
        response = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["role"] == "admin"

    def test_regular_user_role(self, client, test_user_data, db_session):
        """Test regular user has user role."""
        # Create regular user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"]),
            role="user"
        )
        db_session.add(user)
        db_session.commit()

        # Login as user
        login_response = client.post("/api/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]

        # Verify user info shows user role
        response = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["role"] == "user"


class TestPasswordSecurity:
    """Test password hashing and verification."""

    def test_password_not_stored_plaintext(self, client, test_user_data, db_session):
        """Test that passwords are hashed, not stored in plaintext."""
        # Register user
        client.post("/api/auth/register", json={
            "username": test_user_data["username"],
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })

        # Check database
        user = db_session.query(User).filter(User.email == test_user_data["email"]).first()
        assert user.hashed_password != test_user_data["password"]
        assert len(user.hashed_password) > 50  # BCrypt hashes are long

    def test_password_not_exposed_in_response(self, client, test_user_data):
        """Test that password is never exposed in API responses."""
        # Register user
        response = client.post("/api/auth/register", json={
            "username": test_user_data["username"],
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })

        response_text = response.text.lower()
        assert test_user_data["password"].lower() not in response_text
        assert "password" not in response.json()


class TestTokenExpiration:
    """Test JWT token expiration handling."""

    def test_token_contains_expiration(self, client, test_user_data, db_session):
        """Test that JWT token contains expiration claim."""
        from jose import jwt as pyjwt
        from app.core.config import settings

        # Create and login user
        user = User(
            username=test_user_data["username"],
            email=test_user_data["email"],
            hashed_password=hash_password(test_user_data["password"]),
            role="user"
        )
        db_session.add(user)
        db_session.commit()

        login_response = client.post("/api/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token = login_response.json()["access_token"]

        # Decode token without verification to check claims
        decoded = pyjwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert "exp" in decoded
        assert "sub" in decoded
        assert decoded["sub"] == test_user_data["email"]


class TestEmailValidation:
    """Test email validation in authentication system."""

    def test_login_with_invalid_email_format(self, client):
        """Test login rejects invalid email format."""
        response = client.post("/api/auth/login", json={
            "email": "not-an-email",
            "password": "SomePassword123!"
        })

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_with_invalid_email_format(self, client):
        """Test registration rejects invalid email format."""
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "not-an-email",
            "password": "SomePassword123!"
        })

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

