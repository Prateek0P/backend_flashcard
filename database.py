# database.py
from sqlmodel import Session, create_engine
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./flashcards1.db"  # Or your actual DB URL

engine = create_engine(DATABASE_URL, echo=True)

# ✅ Provide the SQLModel base to other files
from sqlmodel import SQLModel

# ✅ Dependency function
def get_db():
    with Session(engine) as session:
        yield session
