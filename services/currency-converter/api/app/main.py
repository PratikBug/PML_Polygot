"""I4 — FastAPI currency conversion service with hardcoded rates."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Currency Converter API", version="1.0.0")

# Hardcoded exchange rates (base: USD)
RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.5,
    "INR": 83.2,
}


class ConvertRequest(BaseModel):
    from_currency: str = Field(..., min_length=3, max_length=3)
    to_currency: str = Field(..., min_length=3, max_length=3)
    amount: float = Field(..., gt=0)

    @field_validator("from_currency", "to_currency")
    @classmethod
    def uppercase_currency(cls, v: str) -> str:
        return v.upper().strip()


class ConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    rate: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/rates")
def list_rates():
    return RATES


@app.post("/convert", response_model=ConvertResponse)
def convert(req: ConvertRequest):
    if req.from_currency not in RATES:
        raise HTTPException(status_code=400, detail=f"Unknown currency: {req.from_currency}")
    if req.to_currency not in RATES:
        raise HTTPException(status_code=400, detail=f"Unknown currency: {req.to_currency}")

    usd_amount = req.amount / RATES[req.from_currency]
    converted = usd_amount * RATES[req.to_currency]
    rate = RATES[req.to_currency] / RATES[req.from_currency]

    return ConvertResponse(
        from_currency=req.from_currency,
        to_currency=req.to_currency,
        amount=req.amount,
        converted_amount=round(converted, 4),
        rate=round(rate, 6),
    )
