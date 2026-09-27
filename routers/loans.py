from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from loan_calculator import (
    calculate_emi,
    check_eligibility,
    generate_emi_schedule,
)
from models import EMISchedule, LoanApplication, User
from schemas import LoanApplicationCreate

router = APIRouter(prefix="/api/loans", tags=["Loans"])


def require_customer(
    request: Request,
    db: Session,
):
    user_id = request.session.get("user_id")

    if not user_id:
        return None, JSONResponse(
            status_code=401,
            content={"detail": "Please log in first"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None, JSONResponse(
            status_code=401,
            content={"detail": "User not found"},
        )

    if user.role != "customer":
        return None, JSONResponse(
            status_code=403,
            content={"detail": "Customer access required"},
        )

    return user, None


@router.post("/apply")
def apply_for_loan(
    request: Request,
    data: LoanApplicationCreate,
    db: Session = Depends(get_db),
):
    user, error = require_customer(request, db)

    if error:
        return error

    emi = calculate_emi(
        data.loan_amount,
        data.interest_rate,
        data.tenure_months,
    )

    eligibility = check_eligibility(
        data.age,
        data.monthly_income,
        emi,
        data.credit_score,
    )

    application = LoanApplication(
        user_id=user.id,
        age=data.age,
        loan_amount=data.loan_amount,
        monthly_income=data.monthly_income,
        interest_rate=data.interest_rate,
        tenure_months=data.tenure_months,
        loan_type=data.loan_type,
        application_date=data.application_date,
        credit_score=data.credit_score,
        emi_amount=emi,
        eligibility_status=eligibility,
        application_status="Pending",
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Loan application submitted",
        "loan_id": application.id,
        "emi_amount": application.emi_amount,
        "eligibility_status": application.eligibility_status,
        "application_status": application.application_status,
    }


@router.get("/me")
def my_loans(
    request: Request,
    db: Session = Depends(get_db),
):
    user, error = require_customer(request, db)

    if error:
        return error

    loans = (
        db.query(LoanApplication)
        .filter(LoanApplication.user_id == user.id)
        .order_by(LoanApplication.id.desc())
        .all()
    )

    return [
        {
            "id": loan.id,
            "loan_type": loan.loan_type,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "tenure_months": loan.tenure_months,
            "emi_amount": loan.emi_amount,
            "eligibility_status": loan.eligibility_status,
            "application_status": loan.application_status,
            "application_date": loan.application_date.isoformat(),
            "credit_score": loan.credit_score,
        }
        for loan in loans
    ]


@router.get("/{loan_id}")
def get_loan(
    loan_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")

    if not user_id:
        return JSONResponse(
            status_code=401,
            content={"detail": "Please log in first"},
        )

    loan = (
        db.query(LoanApplication)
        .filter(LoanApplication.id == loan_id)
        .first()
    )

    if not loan:
        return JSONResponse(
            status_code=404,
            content={"detail": "Loan application not found"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return JSONResponse(
            status_code=401,
            content={"detail": "User not found"},
        )

    if user.role != "admin" and loan.user_id != user.id:
        return JSONResponse(
            status_code=403,
            content={"detail": "You cannot access this loan"},
        )

    schedule = (
        db.query(EMISchedule)
        .filter(EMISchedule.loan_id == loan.id)
        .order_by(EMISchedule.installment_number)
        .all()
    )

    return {
        "id": loan.id,
        "applicant_name": loan.user.name,
        "applicant_email": loan.user.email,
        "loan_type": loan.loan_type,
        "age": loan.age,
        "loan_amount": loan.loan_amount,
        "monthly_income": loan.monthly_income,
        "interest_rate": loan.interest_rate,
        "tenure_months": loan.tenure_months,
        "application_date": loan.application_date.isoformat(),
        "credit_score": loan.credit_score,
        "emi_amount": loan.emi_amount,
        "eligibility_status": loan.eligibility_status,
        "application_status": loan.application_status,
        "emi_schedule": [
            {
                "installment_number": item.installment_number,
                "due_date": item.due_date.isoformat(),
                "principal_amount": item.principal_amount,
                "interest_amount": item.interest_amount,
                "emi_amount": item.emi_amount,
                "remaining_balance": item.remaining_balance,
                "payment_status": item.payment_status,
            }
            for item in schedule
        ],
    }
