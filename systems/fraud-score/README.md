# A3 / D2 — Fraud Score Mini-System

Polyglot mini-system: FastAPI ingestion, Node.js worker, Rust scoring engine.

## Architecture

```
Client → FastAPI API → PostgreSQL
                ↑         ↓
         Node.js Worker polls pending
                ↓
         Rust fraud-scorer CLI (stdin/stdout JSON)
                ↓
         Worker updates score in API/DB
```

## Data Contract

**Input to Rust scorer (stdin JSON):**
```json
{"transaction_id": 1, "user_id": "u1", "amount": 500, "merchant": "Amazon", "currency": "USD"}
```

**Output from Rust scorer (stdout JSON):**
```json
{"transaction_id": 1, "risk_score": 75.0, "risk_level": "high", "factors": ["high_amount"]}
```

## Run Order (Docker)

```bash
docker compose up --build
./scripts/e2e-test.sh
```

## Run Order (Local)

```bash
# 1. Start DB (or use docker compose up db)
# 2. Start API
cd api && pip install -r requirements.txt && uvicorn app.main:app --port 8002

# 3. Build scorer
cd scorer && cargo build --release

# 4. Run worker
cd worker && SCORER_PATH=../scorer/target/release/fraud-scorer node worker.js
```

## Test

```bash
cd api && pytest -v
cd worker && npm test
cd scorer && cargo test
```
