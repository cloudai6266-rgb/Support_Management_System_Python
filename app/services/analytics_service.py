
from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import support_repository, payment_repository


def get_analytics(
    db: Session,
    from_date: date | None = None,
    to_date: date | None = None,
    person_type: str = "ALL",
    person_id: int | None = None
):
    # Default date range
    today = date.today()

    from_date = from_date or today.replace(day=1)
    to_date = to_date or today

    if from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="From date cannot be after To date"
        )

    # Validate person type
    person_type = (person_type or "ALL").upper()

    if person_type not in ["ALL", "CUSTOMER", "SUPPORT"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Person type must be ALL, CUSTOMER or SUPPORT"
        )

    # Get all support assignments
    assignments = support_repository.get_all(db)

    # Apply date and person filters
    filtered = []

    for assignment in assignments:

        if assignment.start_date is None:
            continue

        if not (from_date <= assignment.start_date <= to_date):
            continue

        if person_id is not None:

            customer_id = (
                assignment.customer.id
                if assignment.customer else None
            )

            support_id = (
                assignment.support_person.id
                if assignment.support_person else None
            )

            if person_type == "CUSTOMER":
                if customer_id != person_id:
                    continue

            elif person_type == "SUPPORT":
                if support_id != person_id:
                    continue

            else:
                if (
                    customer_id != person_id
                    and support_id != person_id
                ):
                    continue

        filtered.append(assignment)

    # Initialize totals
    received = Decimal("0.00")
    paid = Decimal("0.00")
    customer_pending = Decimal("0.00")
    support_pending = Decimal("0.00")

    three_days_later = today.fromordinal(today.toordinal() + 3)

    payments_due_in_three_days = 0

    customer_dues = []
    support_dues = []
    upcoming_payments = []

    # Calculate analytics
    for assignment in filtered:

        customer_amount = (
            assignment.agreed_amount or Decimal("0.00")
        )

        support_amount = (
            assignment.support_agreed_amount or Decimal("0.00")
        )

        customer_received = Decimal("0.00")
        support_paid = Decimal("0.00")

        payments = payment_repository.get_by_support_id(
            db,
            assignment.id
        )

        for payment in payments:

            customer_received += (
                payment.amount_received or Decimal("0.00")
            )

            support_paid += (
                payment.amount_paid or Decimal("0.00")
            )

            due_date = payment.next_due_date

            if (
                due_date is not None
                and today <= due_date <= three_days_later
            ):
                payments_due_in_three_days += 1

        received += customer_received
        paid += support_paid

        customer_balance = customer_amount - customer_received
        support_balance = support_amount - support_paid

        if customer_balance > 0:
            customer_pending += customer_balance
            customer_dues.append(assignment)

        if support_balance > 0:
            support_pending += support_balance
            support_dues.append(assignment)

        has_upcoming_payment = any(
            payment.next_due_date is not None
            and today <= payment.next_due_date <= three_days_later
            for payment in payments
        )

        if (
            has_upcoming_payment
            and (
                customer_balance > 0
                or support_balance > 0
            )
        ):
            upcoming_payments.append(assignment)

    # Return analytics results
    return {
        "assignments": filtered,
        "totalReceived": received,
        "totalPaid": paid,
        "netProfit": received - paid,
        "customerPendingDues": customer_pending,
        "supportPaymentsPending": support_pending,
        "paymentsDueInThreeDays": payments_due_in_three_days,
        "customerDues": customer_dues,
        "supportDues": support_dues,
        "upcomingPayments": upcoming_payments
    }
