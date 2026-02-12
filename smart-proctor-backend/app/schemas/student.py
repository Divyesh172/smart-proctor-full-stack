from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
class StudentBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class StudentCreate(StudentBase):
    email: EmailStr
    password: str

# Properties to return via API (Never return the password!)
class Student(StudentBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True # updated for Pydantic v2