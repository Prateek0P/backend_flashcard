from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.deck import DeckCreate, DeckOut
from crud import deck as deck_crud

router = APIRouter()


@router.post("/", response_model=DeckOut)
def create_deck(deck: DeckCreate, db: Session = Depends(get_db),):
    return deck_crud.create_deck(db, deck)

@router.get("/{deck_id}", response_model=DeckOut)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = deck_crud.get_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck

@router.delete("/{deck_id}", response_model=DeckOut)
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = deck_crud.delete_deck(db, deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck

@router.get("/", response_model=list[DeckOut])
def list_decks(
    limit:int = Query(10, ge=1),
    offset: int = Query(0,ge=0),           
    db: Session = Depends(get_db)
    ):
    return deck_crud.get_all_decks(db,limit=limit, offset=offset)
