
from sqlalchemy.orm import Session

from app.repositories import payment_repository
from app.repositories import support_repository


# Create a new payment
def save_payment(db: Session, payment_data: dict):

    support_id = payment_data.get("support_assignment_id")

    if support_id is None:
        raise ValueError("Support assignment ID is required")

    assignment = support_repository.get_by_id(db, support_id)

    if assignment is None:
        raise ValueError(
            f"Support assignment not found with ID: {support_id}"
        )

    return payment_repository.save(db, payment_data, assignment)


# Get all payments
def get_all_payments(db: Session):
    return payment_repository.get_all(db)


# Get payments by support assignment ID
def get_payments_by_support_id(db: Session, support_id: int):
    return payment_repository.get_by_support_id(db, support_id)


# Get payment by ID
def get_payment_by_id(db: Session, payment_id: int):
    return payment_repository.get_by_id(db, payment_id)


# Delete payment
def delete_payment(db: Session, payment_id: int):
    payment = payment_repository.get_by_id(db, payment_id)

    if payment is not None:
        payment_repository.delete(db, payment)


# Update payment
def update_payment(
    db: Session,
    payment_id: int,
    updated_data: dict
):
    existing_payment = get_payment_by_id(db, payment_id)

    if existing_payment is None:
        return None

    existing_payment.amount_received = updated_data["amount_received"]
    existing_payment.received_date = updated_data["received_date"]
    existing_payment.amount_paid = updated_data["amount_paid"]
    existing_payment.paid_date = updated_data["paid_date"]
    existing_payment.next_due_date = updated_data["next_due_date"]
    existing_payment.comments = updated_data["comments"]

    support_id = updated_data.get("support_assignment_id")

    if support_id is not None:
        assignment = support_repository.get_by_id(db, support_id)

        if assignment is None:
            raise ValueError(
                f"Support assignment not found with ID: {support_id}"
            )

        existing_payment.support_assignment = assignment

    return payment_repository.save(db, existing_payment)
