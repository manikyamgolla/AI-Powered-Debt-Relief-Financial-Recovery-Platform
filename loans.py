from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Loan, User
from app.schemas import LoanCreate, LoanUpdate, LoanRead
from app.utils.auth import get_current_user

router = APIRouter(prefix="/loan", tags=["Loans"])


@router.post("", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def create_loan(
    payload: LoanCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    loan = Loan(user_id=current_user.id, **payload.model_dump())
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return loan


@router.get("", response_model=list[LoanRead])
def list_loans(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return session.exec(select(Loan).where(Loan.user_id == current_user.id)).all()


@router.get("/{loan_id}", response_model=LoanRead)
def get_loan(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    loan = _get_owned_loan(loan_id, current_user, session)
    return loan


@router.put("/{loan_id}", response_model=LoanRead)
def update_loan(
    loan_id: int,
    payload: LoanUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    loan = _get_owned_loan(loan_id, current_user, session)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(loan, field, value)
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return loan


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    loan = _get_owned_loan(loan_id, current_user, session)
    session.delete(loan)
    session.commit()


def _get_owned_loan(loan_id: int, current_user: User, session: Session) -> Loan:
    loan = session.get(Loan, loan_id)
    if not loan or loan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
