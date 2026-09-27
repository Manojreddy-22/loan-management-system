from calendar import monthrange
from datetime import date


def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
) -> float:
    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero.")

    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    monthly_rate = annual_interest_rate / 12 / 100

    if monthly_rate == 0:
        return round(principal / tenure_months, 2)

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
        / ((1 + monthly_rate) ** tenure_months - 1)
    )

    return round(emi, 2)


def check_eligibility(
    age: int,
    monthly_income: float,
    emi: float,
    credit_score: int,
) -> str:
    conditions = [
        age >= 21,
        age <= 60,
        monthly_income >= 15000,
        credit_score >= 650,
        emi <= monthly_income * 0.40,
    ]

    return "Eligible" if all(conditions) else "Not Eligible"


def add_months(source_date: date, months: int) -> date:
    month_index = source_date.month - 1 + months
    year = source_date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(
        source_date.day,
        monthrange(year, month)[1],
    )
    return date(year, month, day)


def generate_emi_schedule(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
    start_date: date,
):
    emi = calculate_emi(
        principal,
        annual_interest_rate,
        tenure_months,
    )

    monthly_rate = annual_interest_rate / 12 / 100
    balance = round(principal, 2)
    schedule = []

    for installment_number in range(1, tenure_months + 1):
        if monthly_rate == 0:
            interest = 0.0
            principal_part = emi
        else:
            interest = round(balance * monthly_rate, 2)
            principal_part = round(emi - interest, 2)

        if installment_number == tenure_months:
            principal_part = round(balance, 2)
            actual_emi = round(principal_part + interest, 2)
        else:
            actual_emi = round(emi, 2)

        balance = round(max(balance - principal_part, 0), 2)

        schedule.append(
            {
                "installment_number": installment_number,
                "due_date": add_months(start_date, installment_number),
                "principal_amount": principal_part,
                "interest_amount": interest,
                "emi_amount": actual_emi,
                "remaining_balance": balance,
            }
        )

    return schedule
