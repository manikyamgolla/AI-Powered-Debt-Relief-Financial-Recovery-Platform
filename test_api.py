import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.__enter__()  # triggers startup event (init_db) for the test session


def _register_and_login(email="user@example.com"):
    client.post("/auth/register", json={"name": "Test User", "email": email, "password": "supersecure1"})
    resp = client.post("/auth/login", json={"email": email, "password": "supersecure1"})
    return resp.json()["access_token"]


def test_register_and_login():
    token = _register_and_login("flow@example.com")
    assert token

    resp = client.get("/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "flow@example.com"


def test_loan_crud_and_settlement_flow():
    token = _register_and_login("loanflow@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post(
        "/loan",
        json={
            "lender_name": "Acme Bank",
            "loan_type": "personal",
            "outstanding_amount": 12000,
            "emi": 400,
            "interest_rate": 14.5,
            "overdue_days": 30,
            "tenure_months": 36,
            "status": "overdue",
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    loan_id = create_resp.json()["id"]

    list_resp = client.get("/loan", headers=headers)
    assert len(list_resp.json()) == 1

    settlement_resp = client.post("/settlement", json={"loan_id": loan_id}, headers=headers)
    assert settlement_resp.status_code == 200
    assert 0 < settlement_resp.json()["recommended_percentage"] <= 100

    letter_resp = client.post("/generate-letter", json={"loan_id": loan_id}, headers=headers)
    assert letter_resp.status_code == 200
    assert "Acme Bank" in letter_resp.json()["letter_text"]

    history_resp = client.get("/history", headers=headers)
    assert len(history_resp.json()) == 2
