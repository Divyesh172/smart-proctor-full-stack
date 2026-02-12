from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core.security import create_access_token, verify_password
# Note: You would import your DB session and User model here
# from app.db.session import get_db
# from app.models.user import User

router = APIRouter()

@router.post("/login", response_model=dict)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Standard OAuth2 compatible token login.
    Mentor Note: Using form_data allows integration with Swagger UI 'Authorize' button.
    """

    # 1. FETCH USER (Mocking DB logic for Tuesday Demo)
    # In production: user = db.query(User).filter(User.email == form_data.username).first()
    user_in_db = {"username": "student@college.edu", "hashed_password": "..."} # Simplified

    # 2. VERIFY PASSWORD
    # Note: verify_password handles the salt/hash comparison
    if not user_in_db or not verify_password(form_data.password, user_in_db["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. GENERATE JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_in_db["username"], "role": "student"},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me")
async def read_users_me(
        # current_user: User = Depends(get_current_user)
):
    """
    Returns current student profile.
    Useful for the Next.js frontend to verify session persistence.
    """
    return {"student_id": "12345", "status": "verified"}