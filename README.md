# PML_Polygot — Coding Agent Evaluation Suite

Complete solutions for **"What can you do using a coding agent?"** — all tasks (B1–B6, I1–I6, A1–A6, D1–D6) with runnable code, tests, and documentation.

## Quick Start

```bash
make bootstrap   # install deps for all services
make test        # run all unit tests
make e2e         # run docker-compose end-to-end stack test
```

## Repository Structure

| Path | Task | Description |
|------|------|-------------|
| `services/transaction-api-python/` | B4 | FastAPI transaction service |
| `services/transaction-api-node/` | B5 | Node.js transaction API |
| `services/log-counter-rust/` | B6 | Rust log-level counter CLI |
| `services/currency-converter/` | I4 | FastAPI + Node CLI polyglot pair |
| `systems/fraud-score/` | A3, D2 | Polyglot fraud-score mini-system |
| `infra/` | D1, D4 | Terraform + Kubernetes manifests |
| `observability/` | D6 | Prometheus + Grafana stack |
| `docs/` | B1–B3, I1–I3, I6, A1–A6 | Documentation artifacts |

Full task mapping: [docs/EVAL_INDEX.md](docs/EVAL_INDEX.md)

## I4 — Currency Converter (highlight)

```bash
cd services/currency-converter
./scripts/verify.sh   # one-command proof (API + tests + E2E)
```

See [services/currency-converter/README.md](services/currency-converter/README.md) for API reference and run instructions.

## Verified Tests (Local)

| Service | Tests |
|---------|-------|
| `transaction-api-python` | 11 passed |
| `transaction-api-node` | 5 passed |
| `currency-converter` api/cli | 8 passed |
| `fraud-score` api/worker | 7 passed |

Rust tests run via `cargo test` in CI.
