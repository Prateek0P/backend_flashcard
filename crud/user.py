from sqlmodel import Session, select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from utils.security import hash_password


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)  # hash before calling this if needed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()

def get_user_by_username(db: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()

def delete_user(db: Session, user_id: int) -> User | None:
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


def get_all_users(db: Session) -> list[User]:
    return db.exec(select(User)).all()
