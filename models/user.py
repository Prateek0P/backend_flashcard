from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    role: str = Field(default = "user")
    decks: List["Deck"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all,delete"})
    
    # use string reference
