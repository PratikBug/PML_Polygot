# Evaluation Task Index

Complete mapping of PDF tasks to solutions in this repo.

## Basics (Self-Eval)

| Task | Solution |
|------|----------|
| Repo discovery | `docs/B1-repo-inventory.md` |
| Data model / ER | `docs/I1-er-diagram.md` |
| API mapping | `docs/B2-api-map.md` |
| Flow tracing | `docs/I2-flow-trace.md` |
| Testing | `docs/B3-test-discovery.md` |
| FastAPI greenfield | `services/transaction-api-python/` (B4) |
| Node.js build | `services/transaction-api-node/` (B5) |
| Rust build | `services/log-counter-rust/` (B6) |
| Parallel work | `docs/A1-parallel-plan.md`, `docs/A2-parallel-worktrees.md` |
| Verification | Each doc includes agent vs manual verification |

## Repo Reader & Simple Builder

| ID | Status | Location |
|----|--------|----------|
| B1 | Done | `docs/B1-repo-inventory.md` |
| B2 | Done | `docs/B2-api-map.md` |
| B3 | Done | `docs/B3-test-discovery.md` |
| B4 | Done | `services/transaction-api-python/` — 11 tests passing |
| B5 | Done | `services/transaction-api-node/` — 5 tests passing |
| B6 | Done | `services/log-counter-rust/` — 4 Rust tests |

## Intermediate

| ID | Status | Location |
|----|--------|----------|
| I1 | Done | `docs/I1-er-diagram.md` |
| I2 | Done | `docs/I2-flow-trace.md` |
| I3 | Done | `docs/I3-safe-change.md` + `/transactions/count` endpoint |
| I4 | Done | `services/currency-converter/` — 8 tests passing |
| I5 | Done | Dockerfiles in all services + `systems/fraud-score/docker-compose.yml` |
| I6 | Done | `docs/I6-bug-diagnosis.md` + `app/balance_bug.py` |

## Advanced

| ID | Status | Location |
|----|--------|----------|
| A1 | Done | `docs/A1-parallel-plan.md` |
| A2 | Done | `docs/A2-parallel-worktrees.md` |
| A3 | Done | `systems/fraud-score/` — polyglot mini-system |
| A4 | Done | `docs/A4-modernization.md` + observability module |
| A5 | Done | `docs/A5-code-review.md` |
| A6 | Done | `docs/A6-performance.md` |

## Infra & DevOps

| ID | Status | Location |
|----|--------|----------|
| D1 | Done | `infra/terraform/` |
| D2 | Done | `systems/fraud-score/docker-compose.yml` + `scripts/e2e-test.sh` |
| D3 | Done | `.github/workflows/ci.yml` |
| D4 | Done | `infra/kubernetes/transaction-api.yaml` |
| D5 | Done | `.devcontainer/` + `Makefile bootstrap` |
| D6 | Done | `observability/` — Prometheus + Grafana |

## Verified Test Results (Local)

```
transaction-api-python:  11 passed
transaction-api-node:    5 passed
currency-converter api:  5 passed
currency-converter cli:  3 passed
fraud-score api:         4 passed
fraud-score worker:      3 passed
```

Rust tests run in CI (requires `cargo test`).
