from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import AIHistory, User
from app.schemas import AIHistoryRead
from app.utils.auth import get_current_user

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=list[AIHistoryRead])
def list_history(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return session.exec(
        select(AIHistory)
        .where(AIHistory.user_id == current_user.id)
        .order_by(AIHistory.created_at.desc())
    ).all()


@router.get("/{history_id}", response_model=AIHistoryRead)
def get_history_entry(
    history_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    entry = session.get(AIHistory, history_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="History entry not found")
    return entry
