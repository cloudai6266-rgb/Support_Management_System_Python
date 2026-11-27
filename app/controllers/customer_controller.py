
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services import customer_service
from app.schemas.customer_schema import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("", response_model=list[CustomerResponse])
def get_all(db: Session = Depends(get_db)):
    return customer_service.get_all(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = customer_service.get_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return customer


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create(customer: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.save(db, customer.model_dump())


@router.put("/{customer_id}", response_model=CustomerResponse)
def update(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    updated_customer = customer_service.update(
        db,
        customer_id,
        customer.model_dump()
    )

    if updated_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return updated_customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(customer_id: int, db: Session = Depends(get_db)):
    customer = customer_service.get_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    customer_service.delete(db, customer_id)
    return None
