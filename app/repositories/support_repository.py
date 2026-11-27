
from sqlalchemy.orm import Session, joinedload

from app.models.support import SupportAssignment


def get_all(db: Session):
    return (
        db.query(SupportAssignment)
        .options(
            joinedload(SupportAssignment.customer),
            joinedload(SupportAssignment.support_person)
        )
        .all()
    )


def get_by_id(db: Session, assignment_id: int):
    return (
        db.query(SupportAssignment)
        .options(
            joinedload(SupportAssignment.customer),
            joinedload(SupportAssignment.support_person)
        )
        .filter(SupportAssignment.id == assignment_id)
        .first()
    )


def get_by_status(db: Session, status: str):
    return (
        db.query(SupportAssignment)
        .options(
            joinedload(SupportAssignment.customer),
            joinedload(SupportAssignment.support_person)
        )
        .filter(SupportAssignment.status == status)
        .all()
    )


def get_by_customer_id(db: Session, customer_id: int):
    return (
        db.query(SupportAssignment)
        .options(
            joinedload(SupportAssignment.customer),
            joinedload(SupportAssignment.support_person)
        )
        .filter(SupportAssignment.customer_id == customer_id)
        .all()
    )


def get_by_support_person_id(
    db: Session,
    support_person_id: int
):
    return (
        db.query(SupportAssignment)
        .options(
            joinedload(SupportAssignment.customer),
            joinedload(SupportAssignment.support_person)
        )
        .filter(
            SupportAssignment.support_person_id == support_person_id
        )
        .all()
    )


def save(
    db: Session,
    assignment,
    customer=None,
    support_person=None
):
    if isinstance(assignment, dict):
        assignment = SupportAssignment(**assignment)

    if customer is not None:
        assignment.customer = customer

    if support_person is not None:
        assignment.support_person = support_person

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


def delete_by_id(db: Session, assignment_id: int):
    assignment = get_by_id(db, assignment_id)

    if assignment is not None:
        db.delete(assignment)
        db.commit()
        return True

    return False
