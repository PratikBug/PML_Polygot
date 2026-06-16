# I4 — Polyglot Service Pair: FastAPI + Node CLI

**Evaluation task:** Build a two-component system — a FastAPI service with a `/convert` endpoint and a Node.js CLI client that calls it.

## Architecture

```
Terminal 2                    Terminal 1
┌─────────────┐   POST /convert   ┌──────────────────┐
│  Node CLI   │ ────────────────► │  FastAPI API     │
│  cli.js     │ ◄──────────────── │  hardcoded rates │
└─────────────┘   JSON response   └──────────────────┘
```

## Hardcoded Exchange Rates (base: USD)

| Currency | Rate |
|----------|------|
| USD | 1.0 |
| EUR | 0.92 |
| GBP | 0.79 |
| JPY | 149.5 |
| INR | 83.2 |

## Two-Terminal Run Instructions

### Terminal 1 — Start FastAPI service

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --reload
```

Verify API is up:

```bash
curl http://localhost:8001/health
# {"status":"ok"}
```

### Terminal 2 — Run Node.js CLI client

```bash
cd client
node cli.js USD EUR 100
# 100 USD = 92 EUR (rate: 0.92)
```

More examples:

```bash
node cli.js GBP INR 50
node cli.js USD JPY 10
```

## Input Validation

**API** (`POST /convert`):
- `amount` must be > 0 (422 if negative/zero)
- `from_currency` / `to_currency` must be 3-letter codes
- Unknown currencies return 400

**CLI**:
- Requires 3 args: `<from> <to> <amount>`
- Rejects non-positive amounts

```bash
# API validation
curl -X POST http://localhost:8001/convert \
  -H "Content-Type: application/json" \
  -d '{"from_currency":"USD","to_currency":"EUR","amount":-10}'
# 422 Unprocessable Entity

# CLI validation
node cli.js USD EUR
# Error: Usage: node cli.js <from> <to> <amount>
```

## Tests

### API tests (pytest)

```bash
cd api
pip install -r requirements.txt
pytest -v
```

Expected: **5 passed**

| Test | Verifies |
|------|----------|
| `test_health` | Health endpoint |
| `test_convert_usd_to_eur` | 100 USD → 92 EUR |
| `test_convert_gbp_to_inr` | Cross-currency conversion |
| `test_rejects_unknown_currency` | 400 for XYZ |
| `test_rejects_negative_amount` | 422 for negative |

### Client tests (node:test)

```bash
cd client
npm test
```

Expected: **3 passed**

### Scripted end-to-end verification (one command)

Starts API, runs CLI against it, prints proof, tears down:

```bash
./scripts/verify.sh
```

## API Reference

### `POST /convert`

**Request:**
```json
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 100
}
```

**Response:**
```json
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 100,
  "converted_amount": 92.0,
  "rate": 0.92
}
```

### `GET /rates`

Returns all hardcoded exchange rates.

### `GET /health`

Returns `{"status": "ok"}`.

## Project Structure

```
currency-converter/
├── api/
│   ├── app/main.py          # FastAPI /convert endpoint
│   ├── tests/test_main.py   # 5 API tests
│   └── requirements.txt
├── client/
│   ├── cli.js               # Node.js CLI client
│   ├── cli.test.js          # 3 client tests
│   └── package.json
├── scripts/
│   └── verify.sh            # E2E verification script
└── README.md
```

## I4 Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| FastAPI service with `/convert` | Done | `api/app/main.py` |
| Node.js CLI client calls service | Done | `client/cli.js` |
| Hardcoded rates | Done | `RATES` dict in `main.py` |
| Input validation | Done | Pydantic + CLI arg checks |
| Tests for service | Done | `api/tests/test_main.py` (5 tests) |
| Tests/scripted verification for client | Done | `cli.test.js` + `scripts/verify.sh` |
| README with two-terminal instructions | Done | This file |
