"""Tests for I4 currency converter API."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_convert_usd_to_eur():
    response = client.post("/convert", json={"from_currency": "USD", "to_currency": "EUR", "amount": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["from_currency"] == "USD"
    assert data["to_currency"] == "EUR"
    assert data["converted_amount"] == 92.0


def test_convert_gbp_to_inr():
    response = client.post("/convert", json={"from_currency": "GBP", "to_currency": "INR", "amount": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["converted_amount"] > 0


def test_rejects_unknown_currency():
    response = client.post("/convert", json={"from_currency": "XYZ", "to_currency": "USD", "amount": 100})
    assert response.status_code == 400


def test_rejects_negative_amount():
    response = client.post("/convert", json={"from_currency": "USD", "to_currency": "EUR", "amount": -50})
    assert response.status_code == 422
