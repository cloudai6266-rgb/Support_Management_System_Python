
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.analytics_note import AnalyticsNote
from app.repositories import analytics_note_repository


def get_all_notes(db: Session):
    return analytics_note_repository.get_all(db)


def create_note(db: Session, text: str):
    validate_text(text)

    note = AnalyticsNote(
        note_text=text.strip()
    )

    return analytics_note_repository.save(db, note)


def update_note(db: Session, note_id: int, text: str):
    validate_text(text)

    note = analytics_note_repository.get_by_id(db, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    note.note_text = text.strip()

    return analytics_note_repository.save(db, note)


def delete_note(db: Session, note_id: int):
    note = analytics_note_repository.get_by_id(db, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    analytics_note_repository.delete(db, note)


def validate_text(text: str):
    if text is None or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Note text is required"
        )

    if len(text.strip()) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Note cannot exceed 1000 characters"
        )
