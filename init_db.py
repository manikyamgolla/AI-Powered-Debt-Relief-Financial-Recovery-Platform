"""
Seed the database with a demo user, loans, and financial profile so the app
can be explored immediately after setup.

Usage:
    cd backend && python ../scripts/init_db.py
(run from the backend/ directory so `app` is importable, or add backend to PYTHONPATH)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from sqlmodel import Session, select  # noqa: E402

from app.database import engine, init_db  # noqa: E402
from app.models import FinancialProfile, Loan, LoanStatus, LoanType, User  # noqa: E402
from app.utils.auth import hash_password  # noqa: E402

DEMO_EMAIL = "demo@debtrelief.ai"
DEMO_PASSWORD = "DemoPass123"


def seed():
    init_db()
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == DEMO_EMAIL)).first()
        if existing:
            print("Demo user already exists, skipping seed.")
            return

        user = User(name="Demo User", email=DEMO_EMAIL, hashed_password=hash_password(DEMO_PASSWORD))
        session.add(user)
        session.commit()
        session.refresh(user)

        session.add(
            FinancialProfile(
                user_id=user.id,
                monthly_income=5200,
                monthly_expenses=3100,
                savings=2000,
                monthly_surplus=5200 - 3100,
            )
        )

        session.add_all(
            [
                Loan(
                    user_id=user.id,
                    lender_name="Capital Trust Bank",
                    loan_type=LoanType.credit_card,
                    outstanding_amount=8500,
                    emi=350,
                    interest_rate=22.5,
                    overdue_days=45,
                    tenure_months=24,
                    status=LoanStatus.overdue,
                ),
                Loan(
                    user_id=user.id,
                    lender_name="Metro Auto Finance",
                    loan_type=LoanType.auto,
                    outstanding_amount=14200,
                    emi=420,
                    interest_rate=9.9,
                    overdue_days=0,
                    tenure_months=48,
                    status=LoanStatus.active,
                ),
                Loan(
                    user_id=user.id,
                    lender_name="EduFund Loans",
                    loan_type=LoanType.education,
                    outstanding_amount=6000,
                    emi=180,
                    interest_rate=6.5,
                    overdue_days=15,
                    tenure_months=36,
                    status=LoanStatus.active,
                ),
            ]
        )

        session.commit()
        print(f"Seeded demo user: {DEMO_EMAIL} / {DEMO_PASSWORD}")


if __name__ == "__main__":
    seed()
