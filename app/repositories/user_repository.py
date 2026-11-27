
from sqlalchemy.orm import Session
from app.models.user import User


def save_user(db: Session, user):
    if isinstance(user, dict):
        user = User(**user)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users_by_type(db: Session, user_type: str):
    return db.query(User).filter(User.user_type == user_type).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def email_exists(db: Session, email: str):
    return db.query(User.id).filter(User.email == email).first() is not None


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if user:
        db.delete(user)
        db.commit()
