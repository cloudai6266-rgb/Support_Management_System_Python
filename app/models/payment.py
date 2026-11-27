
from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    Date,
    DateTime,
    String,
    FetchedValue
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # Database column: support_id
    support_assignment_id = Column(
        "support_id",
        Integer,
        ForeignKey("support_assignments.id"),
        nullable=False
    )

    # Relationship with SupportAssignment
    support_assignment = relationship("SupportAssignment")

    amount_received = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    received_date = Column(Date, nullable=True)

    amount_paid = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    paid_date = Column(Date, nullable=True)

    next_due_date = Column(Date, nullable=True)

    comments = Column(String(500), nullable=True)

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=FetchedValue()
    )

    def __repr__(self):
        return (
            f"<Payment(id={self.id}, "
            f"support_assignment_id={self.support_assignment_id}, "
            f"amount_received={self.amount_received}, "
            f"amount_paid={self.amount_paid})>"
        )
