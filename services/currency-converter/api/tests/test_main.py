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


def test_rates_returns_all_currencies():
    response = client.get("/rates")
    assert response.status_code == 200
    rates = response.json()
    assert set(rates.keys()) == {"USD", "EUR", "GBP", "JPY", "INR"}
    assert len(rates) == 5


def test_convert_same_currency_rate_one():
    response = client.post("/convert", json={"from_currency": "USD", "to_currency": "USD", "amount": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["rate"] == 1.0
    assert data["converted_amount"] == 100.0


def test_lowercase_currency_codes_normalized():
    response = client.post("/convert", json={"from_currency": "usd", "to_currency": "eur", "amount": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["from_currency"] == "USD"
    assert data["to_currency"] == "EUR"
    assert data["converted_amount"] == 92.0


def test_rejects_zero_amount():
    response = client.post("/convert", json={"from_currency": "USD", "to_currency": "EUR", "amount": 0})
    assert response.status_code == 422


def test_rejects_invalid_currency_code_length():
    response = client.post("/convert", json={"from_currency": "US", "to_currency": "EUR", "amount": 100})
    assert response.status_code == 422


def test_convert_usd_to_jpy_exact_amount():
    response = client.post("/convert", json={"from_currency": "USD", "to_currency": "JPY", "amount": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["converted_amount"] == 149.5
    assert data["rate"] == 149.5


def test_rejects_unknown_to_currency():
    response = client.post("/convert", json={"from_currency": "USD", "to_currency": "XYZ", "amount": 100})
    assert response.status_code == 400


def test_rejects_missing_required_fields():
    response = client.post("/convert", json={"from_currency": "USD", "amount": 100})
    assert response.status_code == 422
