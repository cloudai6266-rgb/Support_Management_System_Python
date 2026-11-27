
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.support_schema import SupportResponse


class AnalyticsResponse(BaseModel):
    assignments: list[SupportResponse]

    totalReceived: Decimal
    totalPaid: Decimal
    netProfit: Decimal

    customerPendingDues: Decimal
    supportPaymentsPending: Decimal

    paymentsDueInThreeDays: int

    customerDues: list[SupportResponse]
    supportDues: list[SupportResponse]
    upcomingPayments: list[SupportResponse]
