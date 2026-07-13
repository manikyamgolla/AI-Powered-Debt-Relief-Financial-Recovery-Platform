from app.models import Loan, LoanType, LoanStatus
from app.services.finance_service import compute_financial_metrics


def _loan(**overrides):
    defaults = dict(
        id=1,
        user_id=1,
        lender_name="Test Bank",
        loan_type=LoanType.personal,
        outstanding_amount=10000,
        emi=500,
        interest_rate=12.5,
        overdue_days=0,
        tenure_months=24,
        status=LoanStatus.active,
    )
    defaults.update(overrides)
    return Loan(**defaults)


def test_healthy_profile_scores_high():
    loans = [_loan(outstanding_amount=5000, emi=200, overdue_days=0)]
    metrics = compute_financial_metrics(monthly_income=6000, monthly_expenses=2000, loans=loans)
    assert metrics["monthly_surplus"] > 0
    assert metrics["stress_level"] in ("low", "moderate")
    assert 0 <= metrics["health_score"] <= 100


def test_overdue_and_high_emi_lowers_score():
    loans = [_loan(outstanding_amount=50000, emi=2500, overdue_days=90)]
    metrics = compute_financial_metrics(monthly_income=3000, monthly_expenses=2500, loans=loans)
    assert metrics["stress_level"] in ("high", "critical")
    assert metrics["health_score"] < 50


def test_no_loans_no_income_does_not_error():
    metrics = compute_financial_metrics(monthly_income=0, monthly_expenses=0, loans=[])
    assert metrics["total_outstanding"] == 0
    assert metrics["emi_to_income_ratio"] == 0
