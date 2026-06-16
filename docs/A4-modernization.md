# A4 — Repository Modernization Plan

**Repo:** `services/transaction-api-python`

## Findings (with Evidence)

| # | Finding | Evidence | Priority |
|---|---------|----------|----------|
| 1 | In-memory storage — no persistence | `_transactions: List[dict] = []` in `app/main.py:9` | High |
| 2 | No structured logging | No logging imports or calls in `app/main.py` | Medium |
| 3 | No health check depth | `/health` returns static `{"status": "ok"}` without DB check | Medium |
| 4 | No OpenAPI response examples | FastAPI auto-generates but no custom examples | Low |
| 5 | No rate limiting | No middleware for request throttling | Medium |
| 6 | Single-file app structure | All logic in one `main.py` file | Low |

## Prioritized Plan

| Priority | Item | Effort | Risk | Value |
|----------|------|--------|------|-------|
| 1 | Add structured logging | Low | Low | High — enables debugging and observability |
| 2 | Add persistence (SQLite) | Medium | Medium | High — data survives restarts |
| 3 | Enhanced health check | Low | Low | Medium — readiness probes |
| 4 | Rate limiting middleware | Medium | Low | Medium — production safety |
| 5 | Split into modules (routes, models, store) | Medium | Low | Medium — maintainability |
| 6 | OpenAPI examples | Low | None | Low — developer experience |

## First Step Implemented

**Added structured logging** to `observability/api/app/main.py` (D6 deliverable):

- Request counting middleware
- `/metrics` endpoint with structured JSON metrics
- Uptime tracking

This is the highest-value, lowest-risk first step: no breaking changes, additive only, immediately useful for monitoring.

## Verification

```bash
cd observability && docker compose up --build -d
curl http://localhost:8090/metrics
# Returns JSON with transaction_total, http_requests_total, balance_current
```

## Rollback Notes

```bash
# Revert observability changes
git revert <commit-hash>
# Or simply don't deploy the observability service
docker compose -f observability/docker-compose.yml down
```

No changes to the core transaction API — rollback is isolated to the observability module.
