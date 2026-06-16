# B4 — FastAPI Transaction Service

Small Python FastAPI service for tracking transactions and balance.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/transactions` | Create a transaction |
| GET | `/transactions` | List all transactions |
| GET | `/balance` | Current balance |

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Test

```bash
pytest -v
```

## Example

```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "type": "credit", "description": "deposit"}'

curl http://localhost:8000/transactions
curl http://localhost:8000/balance
```
