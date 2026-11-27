
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services import analytics_service
from app.schemas.analytics_schema import AnalyticsResponse


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


@router.get("", response_model=AnalyticsResponse)
def get_analytics(
    fromDate: date | None = None,
    toDate: date | None = None,
    personType: str = "ALL",
    personId: int | None = None,
    db: Session = Depends(get_db)
):
    return analytics_service.get_analytics(
        db=db,
        from_date=fromDate,
        to_date=toDate,
        person_type=personType,
        person_id=personId
    )
