
from sqlalchemy.orm import Session, joinedload

from app.models.payment import Payment
from app.models.support import SupportAssignment


def payment_details_query(db: Session):
    return db.query(Payment).options(
        joinedload(Payment.support_assignment).joinedload(
            SupportAssignment.customer
        ),
        joinedload(Payment.support_assignment).joinedload(
            SupportAssignment.support_person
        )
    )


# Get all payments
def get_all(db: Session):
    return payment_details_query(db).all()


# Get payment by ID
def get_by_id(db: Session, payment_id: int):
    return (
        payment_details_query(db)
        .filter(Payment.id == payment_id)
        .first()
    )


# Get payments by support assignment ID
def get_by_support_id(db: Session, support_id: int):
    return (
        payment_details_query(db)
        .filter(Payment.support_assignment_id == support_id)
        .all()
    )


# Save payment
def save(db: Session, payment, assignment=None):
    if isinstance(payment, dict):
        payment = Payment(**payment)

    if assignment is not None:
        payment.support_assignment = assignment

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return get_by_id(db, payment.id)


# Delete payment
def delete(db: Session, payment):
    db.delete(payment)
    db.commit()
