from database import SessionLocal
from models import User
from security import hash_password


db = SessionLocal()

try:
    admin_email = "admin@loanapp.com"

    existing_admin = (
        db.query(User)
        .filter(User.email == admin_email)
        .first()
    )

    if existing_admin:
        print("Admin already exists.")
    else:
        admin = User(
            name="System Admin",
            email=admin_email,
            mobile="9999999999",
            password_hash=hash_password("admin123"),
            role="admin",
            status="Active",
        )

        db.add(admin)
        db.commit()

        print("Admin created successfully.")
        print("Email: admin@loanapp.com")
        print("Password: admin123")

finally:
    db.close()
