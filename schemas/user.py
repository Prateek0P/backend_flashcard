from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


# Create schema
class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8)

# Output schema (no password)
class UserOut(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

# Update schema (partial update)
class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
