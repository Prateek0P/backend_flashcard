from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

class CardCreate(SQLModel):
    front: str
    back: str
    deck_id: int

class CardUpdate(SQLModel):
    front: Optional[str] = None
    back: Optional[str] = None

class CardOut(SQLModel):
    id: int
    front: str
    back: str
    deck_id: int
    created_at: datetime
    

    
    
