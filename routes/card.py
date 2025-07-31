from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from typing import List,Optional
from crud import card as card_crud
from schemas.card import CardCreate, CardOut, CardUpdate
from dependencies.roles import require_role
from models.user import User

router = APIRouter()

@router.post("/", response_model=CardOut)
def create_card(card: CardCreate, db: Session = Depends(get_db), current_user : User = Depends(require_role("user"))):
    return card_crud.create_card(db, card)

@router.get("/deck/{deck_id}/", response_model=List[CardOut])
def list_cards(
    deck_id: int,   
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),          # Max records to return (default=10, min=1)
    offset: int = Query(0, ge=0),          # How many records to skip (default=0)
    search: Optional[str] = None           # Optional search filter
):
    return card_crud.list_cards(db, limit=limit, offset=offset, deck_id=deck_id, search=search)

@router.get("/{card_id}/", response_model=CardOut)
def get_card(card_id: int, db: Session = Depends(get_db)):
    db_card = card_crud.get_card(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.delete("/{card_id}/", response_model=CardOut)
def delete_card(card_id: int, db: Session = Depends(get_db), current_user : User = Depends(require_role("user"))):
    deleted_card = card_crud.delete_card(db, card_id)
    if not deleted_card:
        raise HTTPException(status_code=404, detail="Card not found")
    if deck.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this card")
    return deleted_card


@router.put("/{card_id}/", response_model=CardOut)
def update_card(card_id: int, card: CardUpdate, db: Session = Depends(get_db),current_user : User = Depends(require_role("user"))):
    updated_card = card_crud.update_card(db, card_id, card)
    if not updated_card:
        raise HTTPException(status_code=404, detail="Card not found")
    if deck.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this deck")
    return updated_card
