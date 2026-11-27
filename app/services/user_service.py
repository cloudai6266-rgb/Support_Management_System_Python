
from datetime import datetime
from sqlalchemy.orm import Session

from app.repositories import user_repository


def save_user(db: Session, user_data: dict):
    if user_repository.email_exists(db, user_data["email"]):
        raise ValueError("Email already exists")

    user_data["registered_at"] = datetime.now()

    return user_repository.save_user(db, user_data)


def get_all_users(db: Session):
    return user_repository.get_all_users(db)


def get_user_by_id(db: Session, user_id: int):
    return user_repository.get_user_by_id(db, user_id)


def get_users_by_type(db: Session, user_type: str):
    return user_repository.get_users_by_type(db, user_type)


def get_user_by_email(db: Session, email: str):
    return user_repository.get_user_by_email(db, email)


def email_exists(db: Session, email: str):
    return user_repository.email_exists(db, email)


def update_user(db: Session, user_id: int, updated_user: dict):
    existing_user = user_repository.get_user_by_id(db, user_id)

    if existing_user is None:
        return None

    if (
        updated_user["email"] != existing_user.email
        and user_repository.email_exists(db, updated_user["email"])
    ):
        raise ValueError("Email already exists")

    existing_user.name = updated_user["name"]
    existing_user.user_type = updated_user["user_type"]
    existing_user.country_code = updated_user["country_code"]
    existing_user.phone = updated_user["phone"]
    existing_user.email = updated_user["email"]
    existing_user.technologies = updated_user["technologies"]

    return user_repository.save_user(db, existing_user)


def delete_user(db: Session, user_id: int):
    user_repository.delete_user(db, user_id)
