"""Tests for fraud-score API (mocks DB layer — no psycopg2 required)."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def mock_db():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    with patch("app.main.get_db", return_value=mock_conn):
        yield mock_conn, mock_cursor


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200


def test_ingest_transaction(mock_db):
    _, cursor = mock_db
    client = TestClient(app)
    cursor.fetchone.return_value = {
        "id": 1,
        "user_id": "user-1",
        "amount": 500.0,
        "merchant": "Amazon",
        "currency": "USD",
        "status": "pending",
        "created_at": "2026-01-01T00:00:00",
    }
    response = client.post(
        "/transactions",
        json={"user_id": "user-1", "amount": 500.0, "merchant": "Amazon"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"


def test_validation_rejects_zero_amount():
    client = TestClient(app)
    response = client.post(
        "/transactions",
        json={"user_id": "user-1", "amount": 0, "merchant": "Test"},
    )
    assert response.status_code == 422


def test_validation_rejects_empty_merchant():
    client = TestClient(app)
    response = client.post(
        "/transactions",
        json={"user_id": "user-1", "amount": 100, "merchant": ""},
    )
    assert response.status_code == 422
