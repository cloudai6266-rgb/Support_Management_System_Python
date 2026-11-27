
from sqlalchemy import Column, Integer, String, DateTime, FetchedValue

from app.database.base import Base


class AnalyticsNote(Base):
    __tablename__ = "analytics_notes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    note_text = Column(
        String(1000),
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=FetchedValue()
    )

    updated_at = Column(
        DateTime,
        nullable=True,
        server_default=FetchedValue(),
        server_onupdate=FetchedValue()
    )
