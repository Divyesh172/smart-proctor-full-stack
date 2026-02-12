from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.integrity import IntegrityViolation

router = APIRouter()

@router.get("/users", response_model=List[schemas.User])
def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve all users. Admin only.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/integrity-logs", response_model=List[schemas.IntegrityLog])
def read_integrity_logs(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get all cheating attempts recorded by Go Bouncer and Python Brain.
    """
    # Direct query to the IntegrityViolation model
    # (Assuming crud.integrity isn't created yet, we use direct DB access or generic CRUD)
    logs = db.query(IntegrityViolation).offset(skip).limit(limit).all()
    return logs

@router.post("/users", response_model=schemas.User)
def create_user_by_admin(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Admin override to create a user manually.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user