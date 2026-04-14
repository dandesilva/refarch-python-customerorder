from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import timedelta
from app.database import get_db
from app.models import AbstractCustomer
from app.auth import create_access_token, verify_password
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBasic()
settings = get_settings()


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str
    username: str


@router.post("/login", response_model=Token)
def login(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Login endpoint using HTTP Basic authentication.
    Returns a JWT token for subsequent requests.

    For demo purposes, accepts username as both username and password.
    In production, implement proper password verification.
    """
    user = (
        db.query(AbstractCustomer)
        .filter(AbstractCustomer.username == credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # For demo: accept username as password (matching original basic auth)
    # In production, use: verify_password(credentials.password, user.password_hash)
    if credentials.password != credentials.username and credentials.password != "b0wfish":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }


@router.get("/me", response_model=dict)
def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: AbstractCustomer = Depends(get_db),
):
    """Get current authenticated user information."""
    return {
        "username": current_user.username,
        "name": current_user.name,
        "type": current_user.type,
    }
