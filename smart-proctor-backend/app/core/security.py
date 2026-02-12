from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# ---------------------------------------------------------
# 1. Password Hashing Engine
# ---------------------------------------------------------
# We use 'bcrypt' because it is resistant to GPU-based attacks.
# 'deprecated="auto"' allows us to rotate hashes in the future
# without breaking existing users.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against the stored hash.
    Used during the Login process (api/auth.py).
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a secure hash for storage in PostgreSQL.
    Used during Student Registration.
    """
    return pwd_context.hash(password)

# ---------------------------------------------------------
# 2. JWT (JSON Web Token) Generation
# ---------------------------------------------------------
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Creates a signed JWT that proves the student's identity.

    Payload Structure:
    - sub (Subject): The Student ID or Email
    - exp (Expiration): When this token dies (CRITICAL for security)
    - type: Explicitly set to 'access' to prevent token confusion attacks
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "access",
        # Add 'iss' (Issuer) to verify it came from YOUR server
        "iss": settings.PROJECT_NAME
    }

    # SIGNING:
    # This is where the magic happens. We verify this signature
    # in the Go WebSocket server using the same SECRET_KEY.
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

# ---------------------------------------------------------
# 3. Token Decoding (Internal Verification)
# ---------------------------------------------------------
def decode_access_token(token: str) -> dict:
    """
    Decodes a token to check validity.
    Used by your 'Brain' (Python) if it needs to verify a
    request coming from the frontend or Go.
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