from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.deck import DeckCreate, DeckOut
from crud import deck as deck_crud
from dependencies.roles import require_role
from models.user import User
from typing import Optional
router = APIRouter()

@router.post("/", response_model=DeckOut)
def create_deck(deck: DeckCreate, db: Session = Depends(get_db),current_user : User = Depends(require_role("user"))):
    return deck_crud.create_deck(db, deck)

@router.get("/{deck_id}", response_model=DeckOut)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = deck_crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck

@router.delete("/{deck_id}", response_model=DeckOut)
def delete_deck(deck_id: int, db: Session = Depends(get_db)
                ,current_user : User = Depends(require_role("user")) ):
    deck = deck_crud.delete_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if deck.user_id != current_user.id and current_user.role != "admin":
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
