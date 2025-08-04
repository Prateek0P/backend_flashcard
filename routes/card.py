from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from typing import List,Optional
from crud import card as card_crud
from schemas.card import CardCreate, CardOut, CardUpdate
from dependencies.roles import require_role
from models.user import User
from auth import get_current_user
from sqlmodel import select
from models.deck import Deck  
from models.card import Card

router = APIRouter()

@router.post("/", response_model=CardOut)
def create_card(card: CardCreate, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    deck = db.exec(select(Deck).where(Deck.id == card.deck_id)).first()

    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if deck.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not the owner of this deck or Admin")
    return card_crud.create_card(db, card)


@router.get("/{card_id}/", response_model=CardOut)
def get_card(card_id: int, db: Session = Depends(get_db)):
    db_card = card_crud.get_card(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.delete("/{card_id}/", response_model=CardOut)
def delete_card(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # fetch the card
    card = db.exec(select(Card).where(Card.id == card_id)).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # fetch the deck
    deck = db.exec(select(Deck).where(Deck.id == card.deck_id)).first()
    if not deck or (deck.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this card")
    return card_crud.delete_card(db, card_id)

@router.put("/{card_id}/", response_model=CardOut)
def update_card(
    card_id: int,
    card: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Fetch the card
    existing_card = db.exec(select(Card).where(Card.id == card_id)).first()
    if not existing_card:
        raise HTTPException(status_code=404, detail="Card not found")

    # 2. Fetch the deck
    deck = db.exec(select(Deck).where(Deck.id == existing_card.deck_id)).first()
    if not deck or (deck.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to update this card")

    # 3. Proceed with update
    return card_crud.update_card(db, card_id, card)
