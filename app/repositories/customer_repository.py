
from sqlalchemy.orm import Session

from app.models.customer import Customer


def get_all(db: Session):
    return db.query(Customer).all()


def get_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(
        Customer.id == customer_id
    ).first()


def save(db: Session, customer):
    if isinstance(customer, dict):
        customer = Customer(**customer)

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def delete(db: Session, customer):
    db.delete(customer)
    db.commit()
