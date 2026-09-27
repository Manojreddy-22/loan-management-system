# Loan Management System

A full-stack Loan Management System built using:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- HTML
- CSS
- JavaScript
- Session authentication
- Argon2 password hashing

## Features

- Customer registration and login
- Admin login
- Password hashing
- Loan application
- Request validation
- EMI calculation
- Eligibility checking
- Customer dashboard
- Admin dashboard
- Approve/reject loan applications
- EMI schedule generation
- PostgreSQL database integration
- REST API endpoints
- Swagger documentation

## Setup

Create a PostgreSQL database named `mydatabase`.

Create `.env` from `.env.example` and add your PostgreSQL credentials.

Install dependencies:

```bash
pip install -r requirements.txt
```

Create an admin:

```bash
python create_admin.py
```

Run:

```bash
uvicorn main:app --reload
```

Open:

- Home: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs

## Demo Admin

Email: `admin@loanapp.com`

Password: `admin123`

Change the demo password before using this outside a local/demo environment.
