from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import AIHistory, AIModuleType, Loan, NegotiationLetter, SettlementRecommendation, User
from app.schemas import LetterRequest, LetterRead
from app.services.ai_service import generate_negotiation_letter
from app.utils.auth import get_current_user

router = APIRouter(tags=["Negotiation Letters"])


@router.post("/generate-letter", response_model=LetterRead)
def create_letter(
    payload: LetterRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    loan = session.get(Loan, payload.loan_id)
    if not loan or loan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Loan not found")

    # Reuse the latest settlement recommendation if one exists, else use outstanding amount.
    latest_settlement = session.exec(
        select(SettlementRecommendation)
        .where(SettlementRecommendation.loan_id == loan.id)
        .order_by(SettlementRecommendation.created_at.desc())
    ).first()

    suggested_amount = latest_settlement.suggested_amount if latest_settlement else loan.outstanding_amount * 0.6
    monthly_payment = latest_settlement.monthly_payment_plan if latest_settlement else loan.emi * 0.5

    letter_text, prompt, used_fallback = generate_negotiation_letter(
        lender_name=loan.lender_name,
        outstanding=loan.outstanding_amount,
        suggested_amount=suggested_amount,
        monthly_payment=monthly_payment,
        letter_type=payload.letter_type,
        tone=payload.tone,
    )

    letter = NegotiationLetter(
        loan_id=loan.id,
        user_id=current_user.id,
        letter_type=payload.letter_type,
        letter_text=letter_text,
    )
    session.add(letter)

    session.add(
        AIHistory(
            user_id=current_user.id,
            module_type=AIModuleType.letter,
            prompt_text=prompt,
            response_text=letter_text,
            used_fallback=used_fallback,
        )
    )
    session.commit()
    session.refresh(letter)
    return letter


@router.get("/letters/{letter_id}", response_model=LetterRead)
def get_letter(
    letter_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    letter = session.get(NegotiationLetter, letter_id)
    if not letter or letter.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Letter not found")
    return letter
