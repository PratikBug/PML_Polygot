"""B4 — FastAPI transaction service with balance tracking."""

from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Transaction API", version="1.0.0")

_transactions: List[dict] = []


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    type: str = Field(..., description="Transaction type: credit or debit")
    description: str = Field(default="", max_length=200)

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        normalized = v.lower().strip()
        if normalized not in ("credit", "debit"):
            raise ValueError("type must be 'credit' or 'debit'")
        return normalized


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    description: str


class BalanceResponse(BaseModel):
    balance: float
    transaction_count: int


class TransactionCountResponse(BaseModel):
    count: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(tx: TransactionCreate):
    record = {
        "id": len(_transactions) + 1,
        "amount": tx.amount,
        "type": tx.type,
        "description": tx.description,
    }
    _transactions.append(record)
    return record


@app.get("/transactions", response_model=List[TransactionResponse])
def list_transactions():
    return _transactions


@app.get("/transactions/count", response_model=TransactionCountResponse)
def get_transaction_count():
    return TransactionCountResponse(count=len(_transactions))


@app.get("/balance", response_model=BalanceResponse)
def get_balance():
    balance = 0.0
    for tx in _transactions:
        if tx["type"] == "credit":
            balance += tx["amount"]
        else:
            balance -= tx["amount"]
    return BalanceResponse(balance=balance, transaction_count=len(_transactions))
