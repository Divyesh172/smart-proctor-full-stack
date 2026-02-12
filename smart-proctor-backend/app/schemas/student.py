from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# ---------------------------------------------------------
# SHARED PROPERTIES
# ---------------------------------------------------------
class StudentBase(BaseModel):
    email: Optional[EmailStr] = Field(None, description="University email address")
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = True
    is_superuser: bool = False

# ---------------------------------------------------------
# INPUT SCHEMAS (Client -> Server)
# ---------------------------------------------------------
class StudentCreate(StudentBase):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Must be at least 8 chars")
    full_name: str

class StudentUpdate(StudentBase):
    password: Optional[str] = Field(None, min_length=8)

# ---------------------------------------------------------
# OUTPUT SCHEMAS (Server -> Client)
# ---------------------------------------------------------
class Student(StudentBase):
    id: int

    # Pydantic V2 Config
    # This allows Pydantic to read data directly from SQLAlchemy models
    class Config:
        from_attributes = True