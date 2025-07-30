from sqlmodel import Session, select
from models.card import Card
from schemas.card import CardCreate, CardUpdate
from typing import List,Optional
from fastapi import Query
from sqlalchemy import or_,func

def create_card(db: Session, card: CardCreate) -> Card:
    new_card = Card(**card.dict())
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

def get_card(db: Session, card_id: int) -> Card | None:
    return db.get(Card, card_id)

def delete_card(db: Session, card_id: int) -> Card | None:
    card = db.get(Card, card_id)
    if card:
        db.delete(card)
        db.commit()
    return card

def update_card(db: Session, card_id: int, card_update: CardUpdate) -> Card | None:
    card = db.get(Card, card_id)
    if not card:
        return None

    update_data = card_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(card, key, value)

    db.commit()
    db.refresh(card)
    return card



def list_cards(
    deck_id: int,
    db: Session,
    
    limit: int = 10,
    offset: int = 0,
    
    search: Optional[str] = None
) -> List[Card]:

    # Start with all cards
    statement = select(Card)

    # Filter by deck if provided
    if deck_id is not None:
        statement = statement.where(Card.deck_id == deck_id)

    # Search by keyword if provided
    if search:
        search_term = f"%{search.lower()}%"
        statement = statement.where(
    or_(
        func.lower(Card.front).like(search_term),
        func.lower(Card.back).like(search_term)
    )
)

    # Apply pagination
    statement = statement.offset(offset).limit(limit)

    return db.exec(statement).all()

