
from datetime import date, datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    AliasChoices,
    model_validator
)


class SupportCreate(BaseModel):
    customer_id: int = Field(
        validation_alias=AliasChoices("customer_id", "customer")
    )

    support_person_id: int = Field(
        validation_alias=AliasChoices(
            "support_person_id", "supportPerson"
        )
    )

    start_date: date = Field(
        validation_alias=AliasChoices("start_date", "startDate")
    )

    end_date: date | None = Field(
        default=None,
        validation_alias=AliasChoices("end_date", "endDate")
    )

    status: str = Field(default="Active", max_length=20)

    agreed_amount: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
        validation_alias=AliasChoices("agreed_amount", "agreedAmount")
    )

    support_agreed_amount: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
        validation_alias=AliasChoices(
            "support_agreed_amount", "supportAgreedAmount"
        )
    )

    support_period_days: int | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "support_period_days", "supportPeriodDays"
        )
    )

    @model_validator(mode="before")
    @classmethod
    def extract_user_ids(cls, values):
        if isinstance(values, dict):
            values = values.copy()

            customer = values.get("customer")
            if isinstance(customer, dict):
                values["customer_id"] = customer.get("id")

            support_person = values.get("supportPerson")
            if isinstance(support_person, dict):
                values["support_person_id"] = support_person.get("id")

        return values


# Details of the customer or support person
class UserDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_type: str = Field(serialization_alias="userType")
    country_code: str | None = Field(
        default=None,
        serialization_alias="countryCode"
    )
    phone: str
    email: str
    registered_at: datetime | None = Field(
        default=None,
        serialization_alias="registeredAt"
    )
    technologies: str | None = None


class SupportResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int

    customer_id: int
    support_person_id: int

    customer: UserDetails

    support_person: UserDetails = Field(
        serialization_alias="supportPerson"
    )

    start_date: date = Field(serialization_alias="startDate")
    end_date: date | None = Field(
        default=None,
        serialization_alias="endDate"
    )

    status: str

    agreed_amount: Decimal = Field(
        serialization_alias="agreedAmount"
    )
    support_agreed_amount: Decimal = Field(
        serialization_alias="supportAgreedAmount"
    )

    support_period_days: int | None = Field(
        default=None,
        serialization_alias="supportPeriodDays"
    )

    created_at: datetime | None = Field(
        default=None,
        serialization_alias="createdAt"
    )
