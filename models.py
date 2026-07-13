from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class LoanStatus(str, Enum):
    active = "active"
    overdue = "overdue"
    settled = "settled"
    closed = "closed"


class LoanType(str, Enum):
    personal = "personal"
    credit_card = "credit_card"
    auto = "auto"
    home = "home"
    education = "education"
    other = "other"


class AIModuleType(str, Enum):
    settlement = "settlement"
    letter = "letter"


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Loans
# ---------------------------------------------------------------------------
class Loan(SQLModel, table=True):
    __tablename__ = "loans"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    lender_name: str
    loan_type: LoanType = Field(default=LoanType.other)
    outstanding_amount: float
    emi: float
    interest_rate: float
    overdue_days: int = Field(default=0)
    tenure_months: int
    status: LoanStatus = Field(default=LoanStatus.active)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Financial Profile
# ---------------------------------------------------------------------------
class FinancialProfile(SQLModel, table=True):
    __tablename__ = "financial_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, unique=True)
    monthly_income: float
    monthly_expenses: float
    savings: float = Field(default=0)
    monthly_surplus: float = Field(default=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Settlement Recommendations
# ---------------------------------------------------------------------------
class SettlementRecommendation(SQLModel, table=True):
    __tablename__ = "settlement_recommendations"

    id: Optional[int] = Field(default=None, primary_key=True)
    loan_id: int = Field(foreign_key="loans.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    recommended_percentage: float
    suggested_amount: float
    monthly_payment_plan: float
    ai_summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Negotiation Letters
# ---------------------------------------------------------------------------
class NegotiationLetter(SQLModel, table=True):
    __tablename__ = "negotiation_letters"

    id: Optional[int] = Field(default=None, primary_key=True)
    loan_id: int = Field(foreign_key="loans.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    letter_type: str = Field(default="settlement_request")
    letter_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# AI History (audit log of all AI prompt/response pairs)
# ---------------------------------------------------------------------------
class AIHistory(SQLModel, table=True):
    __tablename__ = "ai_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    module_type: AIModuleType
    prompt_text: str
    response_text: str
    used_fallback: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
