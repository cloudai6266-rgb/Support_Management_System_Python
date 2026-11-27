
from datetime import date, datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    AliasChoices,
    model_validator
)

from app.schemas.support_schema import SupportResponse


class PaymentCreate(BaseModel):
    support_assignment_id: int = Field(
        validation_alias=AliasChoices(
            "support_assignment_id", "supportAssignment"
        )
    )

    amount_received: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
        validation_alias=AliasChoices(
            "amount_received", "amountReceived"
        )
    )

    received_date: date | None = Field(
        default=None,
        validation_alias=AliasChoices("received_date", "receivedDate")
    )

    amount_paid: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
        validation_alias=AliasChoices("amount_paid", "amountPaid")
    )

    paid_date: date | None = Field(
        default=None,
        validation_alias=AliasChoices("paid_date", "paidDate")
    )

    next_due_date: date | None = Field(
        default=None,
        validation_alias=AliasChoices("next_due_date", "nextDueDate")
    )

    comments: str | None = Field(
        default=None,
        max_length=500
    )

    @model_validator(mode="before")
    @classmethod
    def extract_support_id(cls, values):
        if isinstance(values, dict):
            values = values.copy()

            support = values.get("supportAssignment")
            if isinstance(support, dict):
                values["support_assignment_id"] = support.get("id")

        return values


class PaymentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int

    support_assignment_id: int = Field(
        serialization_alias="supportAssignmentId"
    )

    support_assignment: SupportResponse = Field(
        serialization_alias="supportAssignment"
    )

    amount_received: Decimal = Field(
        serialization_alias="amountReceived"
    )
    received_date: date | None = Field(
        default=None,
        serialization_alias="receivedDate"
    )

    amount_paid: Decimal = Field(
        serialization_alias="amountPaid"
    )
    paid_date: date | None = Field(
        default=None,
        serialization_alias="paidDate"
    )

    next_due_date: date | None = Field(
        default=None,
        serialization_alias="nextDueDate"
    )

    comments: str | None = None

    created_at: datetime | None = Field(
        default=None,
        serialization_alias="createdAt"
    )
