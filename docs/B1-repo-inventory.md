# B1 — Repo Artifact Inventory

**Target repo:** `services/transaction-api-python`  
**Time budget:** 30 minutes

## Classes & Modules

| Artifact | Type | Path |
|----------|------|------|
| `TransactionCreate` | Pydantic Model | `app/main.py` |
| `TransactionResponse` | Pydantic Model | `app/main.py` |
| `BalanceResponse` | Pydantic Model | `app/main.py` |
| `create_transaction` | Controller/Handler | `app/main.py` |
| `list_transactions` | Controller/Handler | `app/main.py` |
| `get_balance` | Controller/Handler | `app/main.py` |
| `health` | Controller/Handler | `app/main.py` |
| `_transactions` | In-memory Store | `app/main.py` |
| `calculate_balance_buggy` | Utility (bug seed) | `app/balance_bug.py` |

## Fraud Score System (`systems/fraud-score`)

| Artifact | Type | Path |
|----------|------|------|
| `TransactionIngest` | Pydantic Model | `api/app/main.py` |
| `ingest_transaction` | Controller | `api/app/main.py` |
| `get_pending_transactions` | Controller | `api/app/main.py` |
| `update_score` | Controller | `api/app/main.py` |
| `transactions` table | DB Entity | `db/init.sql` |
| `risk_scores` table | DB Entity | `db/init.sql` |
| `worker.js` | Background Job | `worker/worker.js` |
| `calculate_risk` | Scoring Service | `scorer/src/lib.rs` |
| `fraud-scorer` | CLI Binary | `scorer/src/main.rs` |

## Config Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container build |
| `docker-compose.yml` | Multi-service orchestration |
| `.github/workflows/ci.yml` | CI pipeline |

## Jobs / Consumers

| Job | Path | Trigger |
|-----|------|---------|
| Fraud worker | `systems/fraud-score/worker/worker.js` | Polls `/transactions/pending` every 5s |
