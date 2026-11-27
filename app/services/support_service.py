
from sqlalchemy.orm import Session

from app.repositories import support_repository
from app.repositories import user_repository


# Create a support assignment
def save_assignment(db: Session, assignment_data: dict):

    customer_id = assignment_data["customer_id"]
    support_person_id = assignment_data["support_person_id"]

    customer = user_repository.get_user_by_id(db, customer_id)

    if customer is None:
        raise ValueError("Customer not found")

    support_person = user_repository.get_user_by_id(
        db, support_person_id
    )

    if support_person is None:
        raise ValueError("Support person not found")

    return support_repository.save(
        db,
        assignment_data,
        customer,
        support_person
    )


# Get all support assignments
def get_all_assignments(db: Session):
    return support_repository.get_all(db)


# Get support assignment by ID
def get_assignment_by_id(db: Session, assignment_id: int):
    return support_repository.get_by_id(db, assignment_id)


# Update support assignment
def update_assignment(
    db: Session,
    assignment_id: int,
    updated_data: dict
):
    existing_assignment = support_repository.get_by_id(
        db, assignment_id
    )

    if existing_assignment is None:
        return None

    customer = user_repository.get_user_by_id(
        db, updated_data["customer_id"]
    )

    if customer is None:
        raise ValueError("Customer not found")

    support_person = user_repository.get_user_by_id(
        db, updated_data["support_person_id"]
    )

    if support_person is None:
        raise ValueError("Support person not found")

    existing_assignment.customer = customer
    existing_assignment.support_person = support_person
    existing_assignment.start_date = updated_data["start_date"]
    existing_assignment.end_date = updated_data["end_date"]
    existing_assignment.status = updated_data["status"]
    existing_assignment.agreed_amount = updated_data["agreed_amount"]
    existing_assignment.support_agreed_amount = updated_data[
        "support_agreed_amount"
    ]
    existing_assignment.support_period_days = updated_data[
        "support_period_days"
    ]

    return support_repository.save(db, existing_assignment)


# Get assignments by status
def get_assignments_by_status(db: Session, status: str):
    return support_repository.get_by_status(db, status)


# Get assignments by customer ID
def get_assignments_by_customer_id(
    db: Session,
    customer_id: int
):
    return support_repository.get_by_customer_id(db, customer_id)


# Get assignments by support person ID
def get_assignments_by_support_person_id(
    db: Session,
    support_person_id: int
):
    return support_repository.get_by_support_person_id(
        db, support_person_id
    )


# Delete support assignment
def delete_assignment(db: Session, assignment_id: int):
    support_repository.delete_by_id(db, assignment_id)
