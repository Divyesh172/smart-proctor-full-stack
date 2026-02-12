from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# ---------------------------------------------------------
# PASSWORD HASHING ENGINE
# ---------------------------------------------------------
# "bcrypt" is the industry standard for password storage.
# We set deprecated="auto" to allow seamless upgrades if we
# change algorithms in the future (without locking users out).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against the stored hash.
    Used during the Login process.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a secure hash for storage in PostgreSQL.
    Used during Registration.
    """
    return pwd_context.hash(password)

# ---------------------------------------------------------
# JWT (JSON WEB TOKEN) FACTORY
# ---------------------------------------------------------
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Creates a signed JWT that proves the user's identity.

    Payload Standard:
    - sub (Subject): The User ID (Primary Key)
    - exp (Expiration): Absolute timestamp when token dies
    - type: Explicitly set to 'access' (prevents token confusion attacks)
    - iss (Issuer): Helps frontend verify source
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "access",
        "iss": settings.PROJECT_NAME
    }

    # SIGNING
    # This uses the SECRET_KEY from .env. If this key leaks,
    # all accounts are compromised. Keep it safe!
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

# ---------------------------------------------------------
# TOKEN VALIDATOR (Internal Tool)
# ---------------------------------------------------------
def decode_access_token(token: str) -> dict:
    """
    Decodes a token to inspect claims manually.
    Useful for debugging or internal service-to-service checks.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token is too old
    except jwt.JWTError:
        return None  # Token is fake/tampered