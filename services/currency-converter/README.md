# I4 — Polyglot Service Pair: FastAPI + Node CLI

**Evaluation task:** Build a two-component system — a FastAPI service with a `/convert` endpoint and a Node.js CLI client that calls it.

## Live Demo (Vercel)

Deploy this folder to Vercel for reviewers:

1. Push repo to GitHub
2. Import in [Vercel](https://vercel.com) — set **Root Directory** to `services/currency-converter` (if monorepo) or repo root
3. Deploy — no env vars required

After deploy:
- **Web UI:** `https://YOUR_APP.vercel.app/` — interactive converter for testers
- **API:** `https://YOUR_APP.vercel.app/health`, `/rates`, `/convert`
- **CLI against production:**
  ```bash
  CONVERTER_API_URL=https://YOUR_APP.vercel.app node client/cli.js USD EUR 100
  ```

### Vercel architecture

```
Browser / CLI  →  /convert, /health, /rates  →  api/index.py (Mangum + FastAPI)
Browser        →  /                           →  public/index.html (web demo)
```

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

## Quick Start (Local)

### One-command verification

```bash
./scripts/verify.sh
```

Runs **15 API tests** + **9 client tests** + live E2E CLI call.

### Two-terminal run

**Terminal 1 — FastAPI:**
```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --reload
```

**Terminal 2 — Node CLI:**
```bash
cd client
node cli.js USD EUR 100
# 100 USD = 92 EUR (rate: 0.92)
```

### All tests

```bash
npm run test:all
# or
cd api && pytest -v          # 15 tests
cd client && npm test        # 9 tests
```

## Test Matrix

### API tests (`api/tests/`) — 15 tests

| Test | Verifies |
|------|----------|
| `test_health` | Health endpoint |
| `test_convert_usd_to_eur` | 100 USD → 92 EUR |
| `test_convert_gbp_to_inr` | Cross-currency conversion |
| `test_rejects_unknown_currency` | 400 for unknown from |
| `test_rejects_negative_amount` | 422 for negative |
| `test_rates_returns_all_currencies` | GET /rates returns 5 currencies |
| `test_convert_same_currency_rate_one` | USD→USD rate 1.0 |
| `test_lowercase_currency_codes_normalized` | usd/eur → USD/EUR |
| `test_rejects_zero_amount` | 422 for amount 0 |
| `test_rejects_invalid_currency_code_length` | 422 for 2-char code |
| `test_convert_usd_to_jpy_exact_amount` | 1 USD = 149.5 JPY |
| `test_rejects_unknown_to_currency` | 400 for unknown to |
| `test_rejects_missing_required_fields` | 422 missing to_currency |
| `test_mangum_handler_is_exported` | Vercel handler exists |
| `test_handler_responds_to_health` | Mangum Lambda event works |

### Client tests (`client/cli.test.js`) — 9 tests

| Suite | Tests |
|-------|-------|
| `parseArgs` | extraction, missing args, lowercase normalize, zero amount, non-numeric |
| `formatResult` | readable output, decimal amounts |
| `convert` | mocked fetch success, API error with detail |

## Input Validation

**API** (`POST /convert`):
- `amount` must be > 0 (422)
- Currencies must be 3-letter codes (422)
- Unknown currencies return 400

**CLI**:
- Requires 3 args: `<from> <to> <amount>`
- Rejects non-positive amounts

## API Reference

### `POST /convert`

```json
// Request
{ "from_currency": "USD", "to_currency": "EUR", "amount": 100 }

// Response
{ "from_currency": "USD", "to_currency": "EUR", "amount": 100, "converted_amount": 92.0, "rate": 0.92 }
```

### `GET /rates` — all hardcoded rates

### `GET /health` — `{"status": "ok"}`

## Project Structure

```
currency-converter/
├── api/
│   ├── app/main.py           # FastAPI /convert endpoint
│   ├── index.py              # Vercel Mangum serverless entry
│   ├── tests/
│   │   ├── test_main.py      # 13 API tests
│   │   └── test_vercel_handler.py  # 2 Vercel tests
│   └── requirements.txt
├── client/
│   ├── cli.js                # Node.js CLI client
│   └── cli.test.js           # 9 client tests
├── public/
│   └── index.html            # Web demo for Vercel reviewers
├── scripts/
│   └── verify.sh             # Full E2E verification
├── vercel.json               # Vercel routes (API + static)
├── package.json              # npm scripts
└── README.md
```

## I4 Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| FastAPI `/convert` | Done | `api/app/main.py` |
| Node.js CLI client | Done | `client/cli.js` |
| Hardcoded rates | Done | `RATES` in `main.py` |
| Input validation | Done | Pydantic + CLI checks |
| Tests for service | Done | 15 API tests |
| Tests/scripted client verification | Done | 9 client tests + `verify.sh` |
| README two-terminal instructions | Done | Above |
| Vercel live demo | Done | `vercel.json` + `public/index.html` |

## Deploy to Vercel

```bash
# From this directory
npx vercel

# Or connect GitHub repo in Vercel dashboard
# Root directory: services/currency-converter (if monorepo)
```

No environment variables required for basic deployment.
