from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    # We enforce that the subject (User ID) must be an integer,
    # matching the primary key in your PostgreSQL database.
    sub: Optional[int] = None