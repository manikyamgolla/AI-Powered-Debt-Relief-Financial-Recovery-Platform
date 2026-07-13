"""Pure financial calculation logic — kept separate from routers so it is
easily unit-testable."""
from typing import List

from app.models import Loan


def compute_financial_metrics(
    monthly_income: float, monthly_expenses: float, loans: List[Loan]
) -> dict:
    total_outstanding = sum(l.outstanding_amount for l in loans)
    total_emi = sum(l.emi for l in loans)
    monthly_surplus = round(monthly_income - monthly_expenses - total_emi, 2)

    emi_to_income_ratio = round((total_emi / monthly_income) * 100, 2) if monthly_income else 0
    debt_to_income_ratio = (
        round((total_outstanding / (monthly_income * 12)) * 100, 2) if monthly_income else 0
    )

    max_overdue = max((l.overdue_days for l in loans), default=0)

    stress_level, health_score = _score(emi_to_income_ratio, debt_to_income_ratio, max_overdue, monthly_surplus)

    return {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "monthly_surplus": monthly_surplus,
        "total_outstanding": round(total_outstanding, 2),
        "total_emi": round(total_emi, 2),
        "emi_to_income_ratio": emi_to_income_ratio,
        "debt_to_income_ratio": debt_to_income_ratio,
        "stress_level": stress_level,
        "health_score": health_score,
    }


def _score(emi_ratio: float, dti_ratio: float, max_overdue: int, surplus: float) -> tuple[str, int]:
    score = 100
    score -= min(emi_ratio, 60)  # heavier EMI burden lowers score
    score -= min(dti_ratio / 2, 25)
    score -= min(max_overdue / 2, 20)
    if surplus < 0:
        score -= 15
    score = max(0, min(100, round(score)))

    if score >= 75:
        stress_level = "low"
    elif score >= 50:
        stress_level = "moderate"
    elif score >= 25:
        stress_level = "high"
    else:
        stress_level = "critical"

    return stress_level, score
