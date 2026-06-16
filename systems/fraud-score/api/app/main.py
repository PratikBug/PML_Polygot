"""A3 — FastAPI fraud-score ingestion API."""

import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Fraud Score API", version="1.0.0")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fraud:fraud@localhost:5432/frauddb")


def get_db():
    import psycopg2
    from psycopg2.extras import RealDictCursor
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


class TransactionIngest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64)
    amount: float = Field(..., gt=0)
    merchant: str = Field(..., min_length=1, max_length=128)
    currency: str = Field(default="USD", min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def uppercase(cls, v: str) -> str:
        return v.upper()


class TransactionResponse(BaseModel):
    id: int
    user_id: str
    amount: float
    merchant: str
    currency: str
    status: str
    created_at: str


class RiskScoreResponse(BaseModel):
    transaction_id: int
    risk_score: float
    risk_level: str
    factors: List[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transactions", response_model=TransactionResponse, status_code=201)
def ingest_transaction(tx: TransactionIngest):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO transactions (user_id, amount, merchant, currency, status) "
                "VALUES (%s, %s, %s, %s, 'pending') RETURNING *",
                (tx.user_id, tx.amount, tx.merchant, tx.currency),
            )
            row = cur.fetchone()
            conn.commit()
            return TransactionResponse(
                id=row["id"],
                user_id=row["user_id"],
                amount=float(row["amount"]),
                merchant=row["merchant"],
                currency=row["currency"],
                status=row["status"],
                created_at=str(row["created_at"]),
            )
    finally:
        conn.close()


@app.get("/transactions/pending")
def get_pending_transactions():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM transactions WHERE status = 'pending' ORDER BY id")
            return cur.fetchall()
    finally:
        conn.close()


@app.put("/transactions/{transaction_id}/score")
def update_score(transaction_id: int, score: RiskScoreResponse):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            status = "flagged" if score.risk_level == "high" else "processed"
            cur.execute(
                "UPDATE transactions SET status = %s, risk_score = %s, risk_level = %s WHERE id = %s",
                (status, score.risk_score, score.risk_level, transaction_id),
            )
            cur.execute(
                "INSERT INTO risk_scores (transaction_id, risk_score, risk_level, factors) "
                "VALUES (%s, %s, %s, %s)",
                (transaction_id, score.risk_score, score.risk_level, ",".join(score.factors)),
            )
            conn.commit()
            return {"updated": True, "transaction_id": transaction_id, "status": status}
    finally:
        conn.close()


@app.get("/transactions/{transaction_id}/score", response_model=Optional[RiskScoreResponse])
def get_score(transaction_id: int):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT transaction_id, risk_score, risk_level, factors FROM risk_scores "
                "WHERE transaction_id = %s ORDER BY id DESC LIMIT 1",
                (transaction_id,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Score not found")
            return RiskScoreResponse(
                transaction_id=row["transaction_id"],
                risk_score=float(row["risk_score"]),
                risk_level=row["risk_level"],
                factors=row["factors"].split(",") if row["factors"] else [],
            )
    finally:
        conn.close()
