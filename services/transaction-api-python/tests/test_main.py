"""Tests for B4 FastAPI transaction service."""

import pytest
from fastapi.testclient import TestClient
from app.main import app, _transactions

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_transactions():
    _transactions.clear()
    yield
    _transactions.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_credit_transaction():
    response = client.post("/transactions", json={"amount": 100.0, "type": "credit", "description": "deposit"})
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100.0
    assert data["type"] == "credit"
    assert data["id"] == 1


def test_create_debit_transaction():
    response = client.post("/transactions", json={"amount": 50.0, "type": "debit"})
    assert response.status_code == 201
    assert response.json()["type"] == "debit"


def test_list_transactions():
    client.post("/transactions", json={"amount": 10.0, "type": "credit"})
    client.post("/transactions", json={"amount": 5.0, "type": "debit"})
    response = client.get("/transactions")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_balance_calculation():
    client.post("/transactions", json={"amount": 100.0, "type": "credit"})
    client.post("/transactions", json={"amount": 30.0, "type": "debit"})
    response = client.get("/balance")
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 70.0
    assert data["transaction_count"] == 2


def test_validation_rejects_negative_amount():
    response = client.post("/transactions", json={"amount": -10.0, "type": "credit"})
    assert response.status_code == 422


def test_validation_rejects_invalid_type():
    response = client.post("/transactions", json={"amount": 10.0, "type": "transfer"})
    assert response.status_code == 422


def test_transaction_count():
    client.post("/transactions", json={"amount": 10.0, "type": "credit"})
    client.post("/transactions", json={"amount": 5.0, "type": "debit"})
    response = client.get("/transactions/count")
    assert response.status_code == 200
    assert response.json()["count"] == 2


def test_transaction_count_empty():
    response = client.get("/transactions/count")
    assert response.status_code == 200
    assert response.json()["count"] == 0
