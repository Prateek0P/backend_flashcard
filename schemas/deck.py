from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from schemas.user import UserOut

# Create schema
class DeckCreate(SQLModel):
    name: str
    description: Optional[str] = None

# Output schema
class DeckOut(SQLModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    owner: Optional[UserOut]
    

# Update schema
class DeckUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

