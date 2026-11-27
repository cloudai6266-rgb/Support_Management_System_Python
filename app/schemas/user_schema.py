from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(max_length=100)
    user_type: str = Field(
        max_length=20,
        validation_alias=AliasChoices("user_type", "userType")
    )
    country_code: str = Field(
        default="+91",
        max_length=5,
        validation_alias=AliasChoices("country_code", "countryCode")
    )
    phone: str = Field(max_length=10)
    email: str = Field(max_length=150)
    technologies: str | None = None


class UserUpdate(BaseModel):
    name: str = Field(max_length=100)
    user_type: str = Field(
        max_length=20,
        validation_alias=AliasChoices("user_type", "userType")
    )
    country_code: str | None = Field(
        default="+91",
        max_length=5,
        validation_alias=AliasChoices("country_code", "countryCode")
    )
    phone: str = Field(max_length=10)
    email: str = Field(max_length=150)
    technologies: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_type: str
    country_code: str | None
    phone: str
    email: str
    registered_at: datetime | None
    technologies: str | None