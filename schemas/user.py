from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel
from pydantic import EmailStr, Field as PydanticField


# Create schema
class UserCreate(SQLModel):
    email: EmailStr
    role: str = "user"
    password: str = PydanticField(min_length=8)

# Output schema (no password)
class UserOut(SQLModel):
    id: int
    email: EmailStr
    role: str 
    created_at: datetime

# Update schema (partial update)
class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = PydanticField(default=None, min_length=8)
