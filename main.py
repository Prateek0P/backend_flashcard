from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
# ✅ Import all models to register them with SQLModel
from models import user, card, deck
from routes import user as user_routes
from routes import card as card_routes
from routes import deck as deck_routes
from routes import auth as auth_routes


# ✅ Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ✅ Include routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(card_routes.router, prefix="/cards", tags=["Cards"])
app.include_router(deck_routes.router, prefix="/decks", tags=["Decks"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

print("FastAPI app is running...")
