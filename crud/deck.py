from sqlmodel import Session, select
from models.deck import Deck
from schemas.deck import DeckCreate, DeckUpdate

def create_deck(db: Session, deck: DeckCreate) -> Deck:
    db_deck = Deck(**deck.dict())
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck

def get_deck(db: Session, deck_id: int) -> Deck | None:
    return db.get(Deck, deck_id)

def delete_deck(db: Session, deck_id: int) -> Deck | None:
    deck = db.get(Deck, deck_id)
    if deck:
        db.delete(deck)
        db.commit()
    return deck

def update_deck(db: Session, deck_id: int, new_data: DeckUpdate) -> Deck | None:
    deck = db.get(Deck, deck_id)
    if not deck:
        return None

    for key, value in new_data.dict(exclude_unset=True).items():
        setattr(deck, key, value)

    db.commit()
    db.refresh(deck)
    return deck

def get_all_decks(db: Session, limit:int, offset: int) -> list[Deck]:
    statement = select(Deck).limit(limit).offset(offset)
    return db.exec(statement).all()
