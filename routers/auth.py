from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import LoginRequest, UserRegister
from security import get_secret_key, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register")
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        return JSONResponse(
            status_code=409,
            content={"detail": "Email is already registered"},
        )

    user = User(
        name=data.name,
        email=data.email,
        mobile=data.mobile,
        password_hash=hash_password(data.password),
        role="customer",
        status="Active",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user_id": user.id,
    }


@router.post("/login")
def login(
    request: Request,
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    email = data.email.strip().lower()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid email or password"},
        )

    if user.status != "Active":
        return JSONResponse(
            status_code=403,
            content={"detail": "Your account is not active"},
        )

    request.session.clear()
    request.session["user_id"] = user.id
    request.session["role"] = user.role

    return {
        "message": "Login successful",
        "role": user.role,
    }


@router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return {
        "message": "Logged out successfully"
    }


@router.get("/me")
def current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")

    if not user_id:
        return JSONResponse(
            status_code=401,
            content={"detail": "Not authenticated"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        request.session.clear()
        return JSONResponse(
            status_code=401,
            content={"detail": "User not found"},
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "mobile": user.mobile,
        "role": user.role,
        "status": user.status,
    }
