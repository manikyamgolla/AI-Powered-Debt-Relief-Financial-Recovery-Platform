from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import FinancialProfile, Loan, User
from app.schemas import FinancialProfileCreate, FinancialAnalysisResult, DashboardSummary
from app.services.finance_service import compute_financial_metrics
from app.utils.auth import get_current_user

router = APIRouter(tags=["Financial Analysis"])


@router.post("/financial-analysis", response_model=FinancialAnalysisResult)
def run_financial_analysis(
    payload: FinancialProfileCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # Upsert the profile
    profile = session.exec(
        select(FinancialProfile).where(FinancialProfile.user_id == current_user.id)
    ).first()

    loans = session.exec(select(Loan).where(Loan.user_id == current_user.id)).all()
    metrics = compute_financial_metrics(payload.monthly_income, payload.monthly_expenses, loans)

    if profile is None:
        profile = FinancialProfile(
            user_id=current_user.id,
            monthly_income=payload.monthly_income,
            monthly_expenses=payload.monthly_expenses,
            savings=payload.savings,
            monthly_surplus=metrics["monthly_surplus"],
        )
    else:
        profile.monthly_income = payload.monthly_income
        profile.monthly_expenses = payload.monthly_expenses
        profile.savings = payload.savings
        profile.monthly_surplus = metrics["monthly_surplus"]

    session.add(profile)
    session.commit()

    return FinancialAnalysisResult(**metrics)


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    profile = session.exec(
        select(FinancialProfile).where(FinancialProfile.user_id == current_user.id)
    ).first()
    loans = session.exec(select(Loan).where(Loan.user_id == current_user.id)).all()

    income = profile.monthly_income if profile else 0
    expenses = profile.monthly_expenses if profile else 0
    metrics = compute_financial_metrics(income, expenses, loans)

    loans_by_status: dict = {}
    for loan in loans:
        loans_by_status[loan.status] = loans_by_status.get(loan.status, 0) + 1

    return DashboardSummary(
        total_loans=len(loans),
        total_outstanding=metrics["total_outstanding"],
        total_emi=metrics["total_emi"],
        monthly_surplus=metrics["monthly_surplus"],
        health_score=metrics["health_score"],
        stress_level=metrics["stress_level"],
        loans_by_status=loans_by_status,
    )


@router.get("/analytics")
def get_analytics(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Data shaped for frontend charts: loan distribution by type, EMI trend."""
    loans = session.exec(select(Loan).where(Loan.user_id == current_user.id)).all()

    by_type: dict = {}
    for loan in loans:
        by_type[loan.loan_type] = by_type.get(loan.loan_type, 0) + loan.outstanding_amount

    emi_series = [{"lender": l.lender_name, "emi": l.emi} for l in loans]

    return {
        "loan_distribution": by_type,
        "emi_series": emi_series,
    }
