from sqlmodel import Session, select
from models.card import Card
from schemas.card import CardCreate, CardUpdate
from typing import List,Optional
from fastapi import Query,Depends
from sqlalchemy import or_,func
from database import get_db

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
    db: Session,
    deck_id: int,
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = None
) -> List[Card]:
    statement = select(Card).where(Card.deck_id == deck_id)

    if search:
        search_term = f"%{search.lower()}%"
        statement = statement.where(
            or_(
                func.lower(Card.front).like(search_term),
                func.lower(Card.back).like(search_term)
            )
        )

    statement = statement.offset(offset).limit(limit)
    return db.exec(statement).all()