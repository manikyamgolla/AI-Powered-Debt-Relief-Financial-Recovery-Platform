"""
AI service layer — wraps calls to the Google Gemini API for two features:
  1. Settlement recommendation generation
  2. Negotiation letter drafting

If the Gemini API is unavailable, times out, or the key is missing, the
service falls back to deterministic templates so the product never
hard-fails for the user.
"""
import json
import logging
from typing import Tuple

from app.core.config import get_settings

logger = logging.getLogger("ai_service")
settings = get_settings()

_client = None


def _get_client():
    """Lazily initialise the Gemini client so the app can boot without a key."""
    global _client
    if _client is not None:
        return _client
    if not settings.GEMINI_API_KEY:
        return None
    try:
        from google import genai

        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return _client
    except Exception as exc:  # pragma: no cover
        logger.warning("Could not initialise Gemini client: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Settlement recommendation
# ---------------------------------------------------------------------------
def build_settlement_prompt(
    income: float, expenses: float, outstanding: float, emi: float, overdue_days: int
) -> str:
    return (
        f"You are a debt settlement advisor. Based on a monthly income of ${income:,.2f} "
        f"and monthly expenses of ${expenses:,.2f}, with a loan outstanding balance of "
        f"${outstanding:,.2f}, current EMI of ${emi:,.2f}, and {overdue_days} overdue days, "
        "suggest a fair settlement percentage (of the outstanding balance) and a realistic "
        "monthly repayment plan the borrower could sustain. Respond ONLY with strict JSON "
        "in this exact shape: "
        '{"recommended_percentage": <number 0-100>, "suggested_amount": <number>, '
        '"monthly_payment_plan": <number>, "reasoning": "<3-4 bullet points as one string, '
        'separated by newlines>"}'
    )


def generate_settlement_recommendation(
    income: float, expenses: float, outstanding: float, emi: float, overdue_days: int
) -> Tuple[dict, str, bool]:
    """Returns (result_dict, raw_prompt, used_fallback)."""
    prompt = build_settlement_prompt(income, expenses, outstanding, emi, overdue_days)
    client = _get_client()

    if client is not None:
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )
            text = (response.text or "").strip()
            text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            data = json.loads(text)
            return data, prompt, False
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini settlement call failed, using fallback: %s", exc)

    # ---- Fallback deterministic logic ----
    surplus = max(income - expenses, 0)
    affordability_ratio = min(surplus / emi, 1) if emi > 0 else 0.5
    # More overdue days / lower affordability -> lower settlement percentage offered
    base_pct = 65 - (overdue_days / 10) + (affordability_ratio * 15)
    recommended_percentage = max(30, min(base_pct, 80))
    suggested_amount = round(outstanding * recommended_percentage / 100, 2)
    monthly_payment_plan = round(min(surplus * 0.5, suggested_amount / 12) or suggested_amount / 12, 2)
    reasoning = (
        "- Calculated using standard affordability heuristics (fallback mode, AI unavailable)\n"
        f"- Surplus of ${surplus:,.2f}/month considered against EMI of ${emi:,.2f}\n"
        f"- {overdue_days} overdue days factored into risk-adjusted settlement percentage\n"
        "- Recommend contacting lender to confirm final negotiated terms"
    )
    data = {
        "recommended_percentage": round(recommended_percentage, 2),
        "suggested_amount": suggested_amount,
        "monthly_payment_plan": monthly_payment_plan,
        "reasoning": reasoning,
    }
    return data, prompt, True


# ---------------------------------------------------------------------------
# Negotiation letters
# ---------------------------------------------------------------------------
def build_letter_prompt(
    lender_name: str,
    outstanding: float,
    suggested_amount: float,
    monthly_payment: float,
    letter_type: str,
    tone: str,
) -> str:
    return (
        f"Write a {tone} email to {lender_name} explaining the borrower's financial hardship "
        f"and proposing a reduced repayment plan. The current outstanding amount is "
        f"${outstanding:,.2f}. The borrower proposes a settlement amount of "
        f"${suggested_amount:,.2f}, payable at approximately ${monthly_payment:,.2f} per month. "
        f"This is a '{letter_type}' letter. Keep it concise, courteous, and lender-specific. "
        "Sign off as 'The Borrower'. Respond with the letter text only, no preamble."
    )


FALLBACK_LETTER_TEMPLATE = """Subject: Request for Loan Settlement - Account Review

Dear {lender_name},

I am writing regarding my outstanding loan balance of ${outstanding:,.2f}. Due to ongoing
financial hardship, I am currently unable to meet the original repayment terms in full.

I would like to propose a settlement amount of ${suggested_amount:,.2f}, to be repaid at
approximately ${monthly_payment:,.2f} per month, which reflects what I can realistically
sustain given my current financial situation.

I value this relationship and am committed to resolving this account responsibly. I would
appreciate the opportunity to discuss this proposal at your earliest convenience.

Thank you for your understanding and consideration.

Sincerely,
The Borrower
"""


def generate_negotiation_letter(
    lender_name: str,
    outstanding: float,
    suggested_amount: float,
    monthly_payment: float,
    letter_type: str = "settlement_request",
    tone: str = "respectful and professional",
) -> Tuple[str, str, bool]:
    """Returns (letter_text, raw_prompt, used_fallback)."""
    prompt = build_letter_prompt(
        lender_name, outstanding, suggested_amount, monthly_payment, letter_type, tone
    )
    client = _get_client()

    if client is not None:
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )
            text = (response.text or "").strip()
            if text:
                return text, prompt, False
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gemini letter call failed, using fallback: %s", exc)

    letter = FALLBACK_LETTER_TEMPLATE.format(
        lender_name=lender_name,
        outstanding=outstanding,
        suggested_amount=suggested_amount,
        monthly_payment=monthly_payment,
    )
    return letter, prompt, True
