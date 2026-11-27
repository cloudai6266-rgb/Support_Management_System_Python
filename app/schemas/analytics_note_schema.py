
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnalyticsNoteCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class AnalyticsNoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    note_text: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
