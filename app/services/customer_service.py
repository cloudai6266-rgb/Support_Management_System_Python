
from sqlalchemy.orm import Session

from app.repositories import customer_repository


def get_all(db: Session):
    return customer_repository.get_all(db)


def get_by_id(db: Session, customer_id: int):
    return customer_repository.get_by_id(db, customer_id)


def save(db: Session, customer_data: dict):
    # Always generate a new ID when creating a customer
    customer_data["id"] = None

    return customer_repository.save(db, customer_data)


def update(db: Session, customer_id: int, updated_data: dict):
    customer = get_by_id(db, customer_id)

    if customer is None:
        return None

    customer.name = updated_data["name"]
    customer.phone = updated_data["phone"]
    customer.email = updated_data["email"]
    customer.address = updated_data["address"]

    return customer_repository.save(db, customer)


def delete(db: Session, customer_id: int):
    customer = get_by_id(db, customer_id)

    if customer is not None:
        customer_repository.delete(db, customer)
