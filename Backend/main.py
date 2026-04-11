from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class LoanRequest(BaseModel):
    name: str
    age: int
    income: float
    loan_amount: float
    interest_rate: float
    tenure: int
    loan_type: str
    application_date: str
    credit_score: int | None = None   # optional

# EMI Calculation
def calculate_emi(P, R, N):
    monthly_rate = R / (12 * 100)
    emi = (P * monthly_rate * (1 + monthly_rate) ** N) / ((1 + monthly_rate) ** N - 1)
    return round(emi, 2)

# Eligibility Logic
def check_eligibility(income, emi, credit_score):
    if credit_score and credit_score < 600:
        return "Rejected (Low Credit Score)"
    elif emi > income * 0.5:
        return "Rejected (High EMI)"
    else:
        return "Eligible"

@app.post("/loan")
def process_loan(data: LoanRequest):
    emi = calculate_emi(data.loan_amount, data.interest_rate, data.tenure)
    status = check_eligibility(data.income, emi, data.credit_score)

    return {
        "name": data.name,
        "loan_type": data.loan_type,
        "emi": emi,
        "status": status,
        "application_date": data.application_date,
        "timestamp": str(datetime.now())
    }