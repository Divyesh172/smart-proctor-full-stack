from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

# ---------------------------------------------------------
# 1. GET CURRENT USER PROFILE
# ---------------------------------------------------------
@router.get("/me", response_model=schemas.User)
def read_user_me(
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    Used by the Frontend to persist session state and show the 'Welcome, [Name]' banner.
    """
    return current_user

# ---------------------------------------------------------
# 2. UPDATE OWN PROFILE
# ---------------------------------------------------------
@router.put("/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)

    # Check if email is being changed and if it is already taken
    if email is not None and email != current_user.email:
        user = crud.user.get_by_email(db, email=email)
        if user:
            raise HTTPException(
                status_code=409,
                detail="This email is already associated with another account.",
            )

    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email

    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user

# ---------------------------------------------------------
# 3. PUBLIC REGISTRATION (SIGN UP)
# ---------------------------------------------------------
@router.post("/open", response_model=schemas.User)
def create_user_open(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )

    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )

    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user