
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Date,
    DateTime,
    FetchedValue
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class SupportAssignment(Base):
    __tablename__ = "support_assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    support_person_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    customer = relationship(
        "User",
        foreign_keys=[customer_id]
    )

    support_person = relationship(
        "User",
        foreign_keys=[support_person_id]
    )

    start_date = Column(Date, nullable=False)

    end_date = Column(Date, nullable=True)

    status = Column(
        String(20),
        nullable=False,
        default="Active"
    )

    agreed_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    support_agreed_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    support_period_days = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=FetchedValue()
    )
