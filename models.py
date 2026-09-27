from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    mobile = Column(String(10), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="customer")
    status = Column(String(20), nullable=False, default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)

    loan_applications = relationship(
        "LoanApplication",
        back_populates="user",
        cascade="all, delete",
    )


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    age = Column(Integer, nullable=False)
    loan_amount = Column(Float, nullable=False)
    monthly_income = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    loan_type = Column(String(50), nullable=False)
    application_date = Column(Date, nullable=False)
    credit_score = Column(Integer, nullable=False)
    emi_amount = Column(Float, nullable=False)
    eligibility_status = Column(String(30), nullable=False)
    application_status = Column(
        String(30),
        nullable=False,
        default="Pending",
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="loan_applications",
    )

    emi_schedule = relationship(
        "EMISchedule",
        back_populates="loan",
        cascade="all, delete",
    )


class EMISchedule(Base):
    __tablename__ = "emi_schedules"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(
        Integer,
        ForeignKey("loan_applications.id", ondelete="CASCADE"),
        nullable=False,
    )
    installment_number = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    principal_amount = Column(Float, nullable=False)
    interest_amount = Column(Float, nullable=False)
    emi_amount = Column(Float, nullable=False)
    remaining_balance = Column(Float, nullable=False)
    payment_status = Column(
        String(20),
        nullable=False,
        default="Pending",
    )

    loan = relationship(
        "LoanApplication",
        back_populates="emi_schedule",
    )
