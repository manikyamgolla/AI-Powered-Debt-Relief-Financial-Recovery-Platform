from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models import LoanStatus, LoanType, AIModuleType


# ---------------- Auth ----------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------------- Loans ----------------
class LoanCreate(BaseModel):
    lender_name: str
    loan_type: LoanType = LoanType.other
    outstanding_amount: float = Field(gt=0)
    emi: float = Field(ge=0)
    interest_rate: float = Field(ge=0)
    overdue_days: int = Field(ge=0, default=0)
    tenure_months: int = Field(gt=0)
    status: LoanStatus = LoanStatus.active


class LoanUpdate(BaseModel):
    lender_name: Optional[str] = None
    loan_type: Optional[LoanType] = None
    outstanding_amount: Optional[float] = None
    emi: Optional[float] = None
    interest_rate: Optional[float] = None
    overdue_days: Optional[int] = None
    tenure_months: Optional[int] = None
    status: Optional[LoanStatus] = None


class LoanRead(BaseModel):
    id: int
    user_id: int
    lender_name: str
    loan_type: LoanType
    outstanding_amount: float
    emi: float
    interest_rate: float
    overdue_days: int
    tenure_months: int
    status: LoanStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------- Financial Profile ----------------
class FinancialProfileCreate(BaseModel):
    monthly_income: float = Field(ge=0)
    monthly_expenses: float = Field(ge=0)
    savings: float = Field(ge=0, default=0)


class FinancialAnalysisResult(BaseModel):
    monthly_income: float
    monthly_expenses: float
    monthly_surplus: float
    total_outstanding: float
    total_emi: float
    emi_to_income_ratio: float
    debt_to_income_ratio: float
    stress_level: str
    health_score: int


# ---------------- Settlement ----------------
class SettlementRequest(BaseModel):
    loan_id: int


class SettlementRead(BaseModel):
    id: int
    loan_id: int
    recommended_percentage: float
    suggested_amount: float
    monthly_payment_plan: float
    ai_summary: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------- Negotiation Letter ----------------
class LetterRequest(BaseModel):
    loan_id: int
    letter_type: str = "settlement_request"
    tone: str = "respectful and professional"


class LetterRead(BaseModel):
    id: int
    loan_id: int
    letter_type: str
    letter_text: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------- History ----------------
class AIHistoryRead(BaseModel):
    id: int
    module_type: AIModuleType
    prompt_text: str
    response_text: str
    used_fallback: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------- Dashboard ----------------
class DashboardSummary(BaseModel):
    total_loans: int
    total_outstanding: float
    total_emi: float
    monthly_surplus: float
    health_score: int
    stress_level: str
    loans_by_status: dict
