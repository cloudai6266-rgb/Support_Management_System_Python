
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services import payment_service
from app.schemas.payment_schema import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/api/payments", tags=["Payments"])


# Get all payments
@router.get("", response_model=list[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    return payment_service.get_all_payments(db)


# Get payments for one support assignment
@router.get("/support/{support_id}", response_model=list[PaymentResponse])
def get_payments_by_support_id(
    support_id: int,
    db: Session = Depends(get_db)
):
    return payment_service.get_payments_by_support_id(db, support_id)


# Get one payment by ID
@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_by_id(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = payment_service.get_payment_by_id(db, payment_id)

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment


# Add a payment
@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    return payment_service.save_payment(db, payment.model_dump())


# Update a payment
@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    updated_payment = payment_service.update_payment(
        db,
        payment_id,
        payment.model_dump()
    )

    if updated_payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return updated_payment


# Delete a payment
@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = payment_service.get_payment_by_id(db, payment_id)

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    payment_service.delete_payment(db, payment_id)
    return None
