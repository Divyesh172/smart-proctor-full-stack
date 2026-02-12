from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

# ---------------------------------------------------------
# 1. OAUTH2 SCHEME CONFIGURATION
# ---------------------------------------------------------
# This tells FastAPI that the client should send the token
# in the 'Authorization' header as 'Bearer <token>'.
# 'tokenUrl' points to the endpoint where the frontend gets the token.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

# ---------------------------------------------------------
# 2. DATABASE SESSION MANAGEMENT (The "Connection Manager")
# ---------------------------------------------------------
def get_db() -> Generator:
    """
    Creates a new database session for each request and closes it
    after the request finishes. This is critical for preventing
    memory leaks in production.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# 3. AUTHENTICATION: GET CURRENT USER
# ---------------------------------------------------------
def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Decodes the JWT, validates it, and fetches the user from the DB.
    If anything is wrong, it raises a 401 Unauthorized error.
    """
    try:
        # A. DECODE TOKEN
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # B. FETCH USER FROM DB
    # We use the 'sub' (subject) claim which contains the user ID
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# ---------------------------------------------------------
# 4. AUTHORIZATION: ACTIVE USER CHECK
# ---------------------------------------------------------
def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Ensures the user hasn't been soft-deleted or banned.
    This is the dependency you will use in most endpoints.
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# ---------------------------------------------------------
# 5. AUTHORIZATION: ADMIN CHECK (RBAC)
# ---------------------------------------------------------
def get_current_active_superuser(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Strictly checks for 'is_superuser' flag.
    Used to protect the Admin Dashboard and Integrity Logs.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user