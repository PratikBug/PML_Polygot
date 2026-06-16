"""D6 — Observability-enabled transaction API with metrics."""

import time
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Observable Transaction API", version="1.0.0")

_transactions: List[dict] = []
_request_count = 0
_start_time = time.time()


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: str = Field(...)
    description: str = Field(default="", max_length=200)

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        normalized = v.lower().strip()
        if normalized not in ("credit", "debit"):
            raise ValueError("type must be 'credit' or 'debit'")
        return normalized


@app.get("/health")
def health():
    return {"status": "ok", "uptime_seconds": round(time.time() - _start_time, 2)}


@app.get("/metrics")
def metrics():
    global _request_count
    credit_count = sum(1 for t in _transactions if t["type"] == "credit")
    debit_count = sum(1 for t in _transactions if t["type"] == "debit")
    balance = sum(t["amount"] if t["type"] == "credit" else -t["amount"] for t in _transactions)
    return {
        "transaction_total": len(_transactions),
        "transaction_credit_total": credit_count,
        "transaction_debit_total": debit_count,
        "balance_current": balance,
        "http_requests_total": _request_count,
        "uptime_seconds": round(time.time() - _start_time, 2),
    }


@app.middleware("http")
async def count_requests(request, call_next):
    global _request_count
    _request_count += 1
    response = await call_next(request)
    return response


@app.post("/transactions", status_code=201)
def create_transaction(tx: TransactionCreate):
    record = {
        "id": len(_transactions) + 1,
        "amount": tx.amount,
        "type": tx.type,
        "description": tx.description,
    }
    _transactions.append(record)
    return record


@app.get("/transactions")
def list_transactions():
    return _transactions


@app.get("/balance")
def get_balance():
    balance = sum(t["amount"] if t["type"] == "credit" else -t["amount"] for t in _transactions)
    return {"balance": balance, "transaction_count": len(_transactions)}
