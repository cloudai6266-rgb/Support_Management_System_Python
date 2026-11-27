
from sqlalchemy.orm import Session

from app.models.analytics_note import AnalyticsNote


def get_all(db: Session):
    return db.query(AnalyticsNote).all()


def get_by_id(db: Session, note_id: int):
    return db.query(AnalyticsNote).filter(
        AnalyticsNote.id == note_id
    ).first()


def save(db: Session, note: AnalyticsNote):
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def delete(db: Session, note: AnalyticsNote):
    db.delete(note)
    db.commit()
