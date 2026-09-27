from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from loan_calculator import generate_emi_schedule
from models import EMISchedule, LoanApplication, User
from schemas import LoanStatusUpdate

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def require_admin(
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

    if not user or user.role != "admin":
        return None, JSONResponse(
            status_code=403,
            content={"detail": "Admin access required"},
        )

    return user, None


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    admin, error = require_admin(request, db)

    if error:
        return error

    user_count = (
        db.query(User)
        .filter(User.role == "customer")
        .count()
    )

    loan_count = db.query(LoanApplication).count()

    approved_count = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.application_status == "Approved"
        )
        .count()
    )

    pending_count = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.application_status == "Pending"
        )
        .count()
    )

    applications = (
        db.query(LoanApplication)
        .order_by(LoanApplication.id.desc())
        .all()
    )

    return {
        "admin_name": admin.name,
        "stats": {
            "customers": user_count,
            "loans": loan_count,
            "approved": approved_count,
            "pending": pending_count,
        },
        "applications": [
            {
                "id": loan.id,
                "applicant_name": loan.user.name,
                "email": loan.user.email,
                "loan_type": loan.loan_type,
                "loan_amount": loan.loan_amount,
                "emi_amount": loan.emi_amount,
                "credit_score": loan.credit_score,
                "eligibility_status": loan.eligibility_status,
                "application_status": loan.application_status,
                "application_date": loan.application_date.isoformat(),
            }
            for loan in applications
        ],
    }


@router.patch("/loans/{loan_id}/status")
def update_loan_status(
    loan_id: int,
    data: LoanStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    _, error = require_admin(request, db)

    if error:
        return error

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

    if data.status == "Approved":
        if loan.eligibility_status != "Eligible":
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "A loan can be approved only when eligibility status is Eligible"
                },
            )

        loan.application_status = "Approved"

        existing_schedule = (
            db.query(EMISchedule)
            .filter(EMISchedule.loan_id == loan.id)
            .first()
        )

        if not existing_schedule:
            schedule_data = generate_emi_schedule(
                loan.loan_amount,
                loan.interest_rate,
                loan.tenure_months,
                loan.application_date,
            )

            for item in schedule_data:
                schedule = EMISchedule(
                    loan_id=loan.id,
                    installment_number=item["installment_number"],
                    due_date=item["due_date"],
                    principal_amount=item["principal_amount"],
                    interest_amount=item["interest_amount"],
                    emi_amount=item["emi_amount"],
                    remaining_balance=item["remaining_balance"],
                    payment_status="Pending",
                )
                db.add(schedule)

    else:
        loan.application_status = "Rejected"

    db.commit()

    return {
        "message": f"Loan marked as {data.status}",
        "loan_id": loan.id,
        "application_status": loan.application_status,
    }
