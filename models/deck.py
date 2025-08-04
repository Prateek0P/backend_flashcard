from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class Deck(SQLModel, table=True):
    __tablename__ = "deck"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(default=None, foreign_key="users.id")

    owner: Optional["User"] = Relationship(back_populates="decks")
    cards: List["Card"] = Relationship(back_populates="deck", sa_relationship_kwargs = {"cascade": "all, delete"})
