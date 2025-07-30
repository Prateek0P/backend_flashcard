from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


# Create schema
class DeckCreate(SQLModel):
    name: str
    description: Optional[str] = None
    owner_id: int

# Output schema
class DeckOut(SQLModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

# Update schema
class DeckUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

