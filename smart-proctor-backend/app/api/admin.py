from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

# ---------------------------------------------------------
# 1. LIST ALL USERS (PAGINATED)
# ---------------------------------------------------------
@router.get("/users", response_model=List[schemas.User])
def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    Only accessible by Superusers (Admins/Proctors).
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

# ---------------------------------------------------------
# 2. CREATE NEW USER (ADMIN OVERRIDE)
# ---------------------------------------------------------
@router.post("/users", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    Admins can create users manually (e.g., bulk uploading a class list).
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

# ---------------------------------------------------------
# 3. INTEGRITY LOGS (THE CHEATER DASHBOARD)
# ---------------------------------------------------------
@router.get("/integrity-logs", response_model=List[schemas.IntegrityLog])
def read_integrity_logs(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get the list of cheating attempts.
    Fetches data from the 'IntegrityViolation' table (populated by the Go Bouncer).
    """
    # Using the CRUD utility to fetch logs in reverse chronological order
    logs = crud.integrity.get_multi(db, skip=skip, limit=limit)
    return logs

# ---------------------------------------------------------
# 4. BAN HAMMER (UPDATE USER STATUS)
# ---------------------------------------------------------
@router.put("/users/{user_id}", response_model=schemas.User)
def update_user_status(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    Used to de-activate (BAN) a student caught cheating.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user