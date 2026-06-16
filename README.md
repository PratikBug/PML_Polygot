# I4 — Currency Converter (Polyglot: FastAPI + Node CLI)

Evaluation submission for **I4: Polyglot service pair — FastAPI plus Node client**.

## What this is

A two-component currency converter:
- **FastAPI** backend with `POST /convert` and hardcoded exchange rates
- **Node.js CLI** client that calls the API
- **Web demo** (`public/index.html`) for live reviewer testing on Vercel

## Quick proof (one command)

```bash
cd services/currency-converter
./scripts/verify.sh
```

**Result:** 15 API tests + 9 client tests + live E2E — all green.

## Test summary

| Component | Tests | Command |
|-----------|-------|---------|
| FastAPI API | 15 | `cd api && pytest -v` |
| Node CLI | 9 | `cd client && npm test` |
| E2E script | API + CLI + curl | `./scripts/verify.sh` |

## Two-terminal demo (local)

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

## Vercel deployment (for reviewers)

1. Push to GitHub
2. Import in Vercel — root directory: `services/currency-converter`
3. Share URL — reviewers get web UI + live API

```bash
CONVERTER_API_URL=https://YOUR_APP.vercel.app node client/cli.js USD EUR 100
```

## Project layout

```
services/currency-converter/
├── api/                 # FastAPI + Mangum (Vercel)
├── client/              # Node CLI (I4 requirement)
├── public/index.html    # Web demo for testers
├── scripts/verify.sh    # Full verification
├── vercel.json
└── README.md            # Full documentation
```

Full docs: [services/currency-converter/README.md](services/currency-converter/README.md)
