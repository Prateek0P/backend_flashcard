from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    front: str
    back: str
    deck_id: int = Field(foreign_key="deck.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    deck: Optional["Deck"] = Relationship(back_populates="cards")
