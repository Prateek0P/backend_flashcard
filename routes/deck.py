from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.deck import DeckCreate, DeckOut
from crud import deck as deck_crud
from crud import card as card_crud
from dependencies.roles import require_role
from models.user import User
from typing import Optional, List
from auth import get_current_user
from models.deck import Deck
from schemas.card import CardOut

router = APIRouter()

@router.post("/", response_model=DeckOut)
def create_deck(deck: DeckCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return deck_crud.create_deck(db, deck, current_user.id)

@router.get("/{deck_id}", response_model=DeckOut)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = deck_crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck

@router.delete("/{deck_id}", response_model=DeckOut)
def delete_deck(deck_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    deck = deck_crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if deck.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this deck")
    return deck_crud.delete_deck(db, deck_id)


@router.get("/", response_model=list[DeckOut])
def list_decks(
    db: Session = Depends(get_db),
    limit:int = Query(10, ge=1),
    offset: int = Query(0,ge=0),   
    search: Optional[str] = None        
    ):
    return deck_crud.get_all_decks(db,limit=limit, offset=offset,search= search)
@router.put("/{deck_id}", response_model=DeckOut)
def update_deck(
    deck_id: int,
    new_deck: DeckCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deck = deck_crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if deck.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this deck")

    updated_deck = deck_crud.update_deck(db, deck_id, new_deck)
    return updated_deck


@router.get("/showcards/{deck_id}/", response_model=List[CardOut])
def list_cards(
    deck_id: int,   
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),          # Max records to return (default=10, min=1)
    offset: int = Query(0, ge=0),          # How many records to skip (default=0)
    search: Optional[str] = None           # Optional search filter
):
    return card_crud.list_cards(db, limit=limit, offset=offset, deck_id=deck_id, search=search)
