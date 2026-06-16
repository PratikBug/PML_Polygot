# A1 — Multi-Worktree Parallel Plan

**Task:** Add observability metrics endpoint + add transaction count endpoint in parallel

## Task Decomposition

| Lane | Task | Scope |
|------|------|-------|
| Lane A | Add `/metrics` endpoint to transaction API | `services/transaction-api-python/` |
| Lane B | Add `/transactions/count` endpoint | `services/transaction-api-python/` |

## Worktree / Branch Names

| Lane | Branch | Worktree Path |
|------|--------|---------------|
| A | `feat/metrics-endpoint` | `../coding-agent-eval-metrics` |
| B | `feat/transaction-count` | `../coding-agent-eval-count` |

## Agent Prompts

**Lane A:**
> Add a GET /metrics endpoint to services/transaction-api-python/app/main.py that returns JSON with transaction_count, credit_count, debit_count, and balance. Add tests in tests/test_main.py. Do not modify existing endpoints.

**Lane B:**
> Add a GET /transactions/count endpoint to services/transaction-api-python/app/main.py that returns {"count": N}. Add a test. Do not modify existing endpoints or add metrics.

## Shared Constraints

- Only modify files in `services/transaction-api-python/`
- All existing tests must continue passing
- No new dependencies
- Follow existing Pydantic model patterns
- Run `pytest -v` before committing

## Merge Order

1. Merge Lane B first (`feat/transaction-count`) — smaller, isolated route
2. Merge Lane A second (`feat/metrics-endpoint`) — no file overlap with B

## Conflict / Risk Plan

| Risk | Mitigation |
|------|------------|
| Both lanes edit `app/main.py` | Sequential merge; resolve import/model additions |
| Both lanes edit `tests/test_main.py` | Add tests at end of file; minimal conflict |
| Test fixture interference | Each lane runs tests independently before merge |

## Verification Plan

```bash
git merge feat/transaction-count
pytest services/transaction-api-python/ -v
git merge feat/metrics-endpoint
pytest services/transaction-api-python/ -v
make test
```
