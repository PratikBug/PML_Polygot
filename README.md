# I4 — Currency Converter (Polyglot: FastAPI + Node CLI)

Evaluation submission for **I4: Polyglot service pair — FastAPI plus Node client**.

## Quick Start

```bash
cd services/currency-converter

# One-command proof (starts API, runs all tests + E2E)
./scripts/verify.sh
```

## Two-Terminal Demo

**Terminal 1:**
```bash
cd services/currency-converter/api
pip install -r requirements.txt
uvicorn app.main:app --port 8001
```

**Terminal 2:**
```bash
cd services/currency-converter/client
node cli.js USD EUR 100
```

## Full documentation

See [services/currency-converter/README.md](services/currency-converter/README.md) for API reference, validation rules, test matrix, and I4 checklist.

## What's in this submission

| Component | Path |
|-----------|------|
| FastAPI `/convert` service | `services/currency-converter/api/` |
| Node.js CLI client | `services/currency-converter/client/` |
| E2E verify script | `services/currency-converter/scripts/verify.sh` |
