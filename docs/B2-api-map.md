# B2 — API Endpoint Map

**Target repos:** All services in this monorepo

## `services/transaction-api-python` (B4)

| Method | Route | Handler | Source |
|--------|-------|---------|--------|
| GET | `/health` | `health()` | `app/main.py:39` |
| POST | `/transactions` | `create_transaction()` | `app/main.py:44` |
| GET | `/transactions` | `list_transactions()` | `app/main.py:56` |
| GET | `/balance` | `get_balance()` | `app/main.py:61` |

## `services/transaction-api-node` (B5)

| Method | Route | Handler | Source |
|--------|-------|---------|--------|
| GET | `/health` | inline handler | `src/index.js:26` |
| POST | `/transactions` | inline handler | `src/index.js:30` |
| GET | `/transactions` | inline handler | `src/index.js:45` |
| GET | `/balance` | inline handler | `src/index.js:49` |

## `services/currency-converter/api` (I4)

| Method | Route | Handler | Source |
|--------|-------|---------|--------|
| GET | `/health` | `health()` | `api/app/main.py:39` |
| GET | `/rates` | `list_rates()` | `api/app/main.py:44` |
| POST | `/convert` | `convert()` | `api/app/main.py:49` |

## `systems/fraud-score/api` (A3)

| Method | Route | Handler | Source |
|--------|-------|---------|--------|
| GET | `/health` | `health()` | `api/app/main.py:51` |
| POST | `/transactions` | `ingest_transaction()` | `api/app/main.py:56` |
| GET | `/transactions/pending` | `get_pending_transactions()` | `api/app/main.py:81` |
| PUT | `/transactions/{id}/score` | `update_score()` | `api/app/main.py:92` |
| GET | `/transactions/{id}/score` | `get_score()` | `api/app/main.py:112` |

## `observability/api` (D6)

| Method | Route | Handler | Source |
|--------|-------|---------|--------|
| GET | `/health` | `health()` | `observability/api/app/main.py:30` |
| GET | `/metrics` | `metrics()` | `observability/api/app/main.py:35` |
| POST | `/transactions` | `create_transaction()` | `observability/api/app/main.py:58` |
| GET | `/transactions` | `list_transactions()` | `observability/api/app/main.py:71` |
| GET | `/balance` | `get_balance()` | `observability/api/app/main.py:76` |
