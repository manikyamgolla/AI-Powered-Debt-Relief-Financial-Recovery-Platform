from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import AIHistory, AIModuleType, FinancialProfile, Loan, SettlementRecommendation, User
from app.schemas import SettlementRequest, SettlementRead
from app.services.ai_service import generate_settlement_recommendation
from app.utils.auth import get_current_user

router = APIRouter(prefix="/settlement", tags=["Settlement"])


@router.post("", response_model=SettlementRead)
def create_settlement_recommendation(
    payload: SettlementRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    loan = session.get(Loan, payload.loan_id)
    if not loan or loan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Loan not found")

    profile = session.exec(
        select(FinancialProfile).where(FinancialProfile.user_id == current_user.id)
    ).first()
    income = profile.monthly_income if profile else 0
    expenses = profile.monthly_expenses if profile else 0

    result, prompt, used_fallback = generate_settlement_recommendation(
        income=income,
        expenses=expenses,
        outstanding=loan.outstanding_amount,
        emi=loan.emi,
        overdue_days=loan.overdue_days,
    )

    recommendation = SettlementRecommendation(
        loan_id=loan.id,
        user_id=current_user.id,
        recommended_percentage=result["recommended_percentage"],
        suggested_amount=result["suggested_amount"],
        monthly_payment_plan=result["monthly_payment_plan"],
        ai_summary=result["reasoning"],
    )
    session.add(recommendation)

    session.add(
        AIHistory(
            user_id=current_user.id,
            module_type=AIModuleType.settlement,
            prompt_text=prompt,
            response_text=str(result),
            used_fallback=used_fallback,
        )
    )
    session.commit()
    session.refresh(recommendation)
    return recommendation


@router.get("/{recommendation_id}", response_model=SettlementRead)
def get_settlement_recommendation(
    recommendation_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    rec = session.get(SettlementRecommendation, recommendation_id)
    if not rec or rec.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return rec
