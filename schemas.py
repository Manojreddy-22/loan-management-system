from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    mobile: str
    password: str = Field(min_length=6, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name is required")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Enter a valid email address")
        return value

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str) -> str:
        value = value.strip()
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Mobile number must contain exactly 10 digits")
        return value


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=100)


class LoanApplicationCreate(BaseModel):
    age: int = Field(ge=18, le=100)
    loan_amount: float = Field(gt=0, le=50000000)
    monthly_income: float = Field(gt=0, le=100000000)
    interest_rate: float = Field(ge=0, le=50)
    tenure_months: int = Field(ge=1, le=360)
    loan_type: str = Field(min_length=2, max_length=50)
    application_date: date
    credit_score: int = Field(ge=300, le=900)

    @field_validator("loan_type")
    @classmethod
    def validate_loan_type(cls, value: str) -> str:
        allowed = {
            "Personal",
            "Home",
            "Education",
            "Vehicle",
            "Business",
        }
        value = value.strip().title()
        if value not in allowed:
            raise ValueError(
                "Loan type must be Personal, Home, Education, Vehicle, or Business"
            )
        return value


class LoanStatusUpdate(BaseModel):
    status: Literal["Approved", "Rejected"]


class LoanResponse(BaseModel):
    id: int
    user_id: int
    applicant_name: str
    loan_type: str
    loan_amount: float
    monthly_income: float
    interest_rate: float
    tenure_months: int
    application_date: date
    credit_score: int
    emi_amount: float
    eligibility_status: str
    application_status: str
