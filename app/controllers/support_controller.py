
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services import support_service
from app.schemas.support_schema import SupportCreate, SupportResponse

router = APIRouter(
    prefix="/api/support",
    tags=["Support"]
)


@router.get("", response_model=list[SupportResponse])
def get_all_assignments(db: Session = Depends(get_db)):
    return support_service.get_all_assignments(db)


@router.get("/{assignment_id}", response_model=SupportResponse)
def get_assignment_by_id(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = support_service.get_assignment_by_id(db, assignment_id)

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support assignment not found"
        )

    return assignment


@router.post("", response_model=SupportResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(
    assignment: SupportCreate,
    db: Session = Depends(get_db)
):
    try:
        return support_service.save_assignment(
            db, assignment.model_dump()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{assignment_id}", response_model=SupportResponse)
def update_assignment(
    assignment_id: int,
    assignment: SupportCreate,
    db: Session = Depends(get_db)
):
    try:
        updated = support_service.update_assignment(
            db, assignment_id, assignment.model_dump()
        )

        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Support assignment not found"
            )

        return updated

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    deleted = support_service.delete_assignment(db, assignment_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support assignment not found"
        )

    return None
