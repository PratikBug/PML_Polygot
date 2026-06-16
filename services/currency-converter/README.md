# I4 — Currency Converter (FastAPI + Node CLI)

Two-component system: FastAPI `/convert` endpoint and Node.js CLI client.

## Two-Terminal Run Instructions

### Terminal 1 — Start API

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --port 8001
```

### Terminal 2 — Run CLI Client

```bash
cd client
node cli.js USD EUR 100
```

## Test

```bash
cd api && pytest -v
cd client && npm test
```
