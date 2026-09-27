import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database import Base, engine
from routers import admin, auth, loans
from security import get_secret_key

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loan Management System",
    description="Full-stack Loan Management System using FastAPI, SQLAlchemy and PostgreSQL",
    version="1.0.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=get_secret_key(),
    same_site="lax",
    https_only=False,
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(loans.router)
app.include_router(admin.router)


@app.get("/")
def home(request: Request):
    user_id = request.session.get("user_id")
    role = request.session.get("role")

    if user_id and role == "admin":
        return RedirectResponse(
            url="/admin/dashboard",
            status_code=303,
        )

    if user_id:
        return RedirectResponse(
            url="/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/login")
def login_page(request: Request):
    if request.session.get("user_id"):
        role = request.session.get("role")

        if role == "admin":
            return RedirectResponse(
                url="/admin/dashboard",
                status_code=303,
            )

        return RedirectResponse(
            url="/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request},
    )


@app.get("/register")
def register_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(
            url="/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request},
    )


@app.get("/dashboard")
def customer_dashboard(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    if request.session.get("role") == "admin":
        return RedirectResponse(
            url="/admin/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="customer_dashboard.html",
        context={"request": request},
    )


@app.get("/apply-loan")
def apply_loan_page(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    if request.session.get("role") == "admin":
        return RedirectResponse(
            url="/admin/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="apply_loan.html",
        context={"request": request},
    )


@app.get("/loan/{loan_id}")
def loan_details_page(
    loan_id: int,
    request: Request,
):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="loan_details.html",
        context={
            "request": request,
            "loan_id": loan_id,
        },
    )


@app.get("/admin/dashboard")
def admin_dashboard_page(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    if request.session.get("role") != "admin":
        return RedirectResponse(
            url="/dashboard",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={"request": request},
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Loan Management System is running",
    }
