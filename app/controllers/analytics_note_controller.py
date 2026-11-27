
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services import analytics_note_service
from app.schemas.analytics_note_schema import (
    AnalyticsNoteCreate,
    AnalyticsNoteResponse
)

router = APIRouter(
    prefix="/api/analytics/notes",
    tags=["Analytics Notes"]
)


@router.get("", response_model=list[AnalyticsNoteResponse])
def get_all_notes(db: Session = Depends(get_db)):
    return analytics_note_service.get_all_notes(db)


@router.post(
    "",
    response_model=AnalyticsNoteResponse,
    status_code=status.HTTP_201_CREATED
)
def create_note(
    request: AnalyticsNoteCreate,
    db: Session = Depends(get_db)
):
    return analytics_note_service.create_note(
        db,
        request.text
    )


@router.put(
    "/{note_id}",
    response_model=AnalyticsNoteResponse
)
def update_note(
    note_id: int,
    request: AnalyticsNoteCreate,
    db: Session = Depends(get_db)
):
    return analytics_note_service.update_note(
        db,
        note_id,
        request.text
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    analytics_note_service.delete_note(db, note_id)
    return None
