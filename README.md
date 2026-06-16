# Coding Agent Evaluation Solutions

Complete solutions for the **"What can you do using a coding agent?"** evaluation document. Every task (B1–B6, I1–I6, A1–A6, D1–D6) has runnable code, tests, and documentation artifacts.

## Quick Start (D5 — single command bootstrap)

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
| `services/currency-converter/` | I4 | FastAPI + Node CLI pair |
| `systems/fraud-score/` | A3, D2 | Polyglot fraud-score mini-system |
| `infra/terraform/` | D1 | Terraform (S3 + Lambda + API Gateway) |
| `infra/kubernetes/` | D4 | K8s manifests for transaction API |
| `observability/` | D6 | Prometheus + Grafana stack |
| `docs/` | B1–B3, I1–I3, I6, A1–A6 | Analysis artifacts |
| `.github/workflows/` | D3 | CI pipeline |
| `.devcontainer/` | D5 | Reproducible dev environment |

## Documentation Index

| Doc | Task |
|-----|------|
| [docs/B1-repo-inventory.md](docs/B1-repo-inventory.md) | B1 — Repo artifact inventory |
| [docs/B2-api-map.md](docs/B2-api-map.md) | B2 — API endpoint map |
| [docs/B3-test-discovery.md](docs/B3-test-discovery.md) | B3 — Test discovery & execution |
| [docs/I1-er-diagram.md](docs/I1-er-diagram.md) | I1 — ER diagram from code |
| [docs/I2-flow-trace.md](docs/I2-flow-trace.md) | I2 — End-to-end flow trace |
| [docs/I3-safe-change.md](docs/I3-safe-change.md) | I3 — Small safe change |
| [docs/I6-bug-diagnosis.md](docs/I6-bug-diagnosis.md) | I6 — Bug diagnosis |
| [docs/A1-parallel-plan.md](docs/A1-parallel-plan.md) | A1 — Multi-worktree plan |
| [docs/A2-parallel-worktrees.md](docs/A2-parallel-worktrees.md) | A2 — Parallel worktrees execution |
| [docs/A4-modernization.md](docs/A4-modernization.md) | A4 — Modernization plan |
| [docs/A5-code-review.md](docs/A5-code-review.md) | A5 — Agent code review |
| [docs/A6-performance.md](docs/A6-performance.md) | A6 — Performance profiling |

## Per-Service Commands

### B4 — Python FastAPI (`services/transaction-api-python`)

```bash
cd services/transaction-api-python
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -v
```

### B5 — Node.js (`services/transaction-api-node`)

```bash
cd services/transaction-api-node
npm install
npm start
npm test
```

### B6 — Rust (`services/log-counter-rust`)

```bash
cd services/log-counter-rust
cargo build
cargo test
cargo run -- sample.log
```

### I4 — Currency Converter

```bash
# Terminal 1
cd services/currency-converter/api && pip install -r requirements.txt && uvicorn app.main:app --port 8001

# Terminal 2
cd services/currency-converter/client && npm install && node cli.js USD EUR 100
```

### A3 / D2 — Fraud Score System

```bash
cd systems/fraud-score
docker compose up --build
./scripts/e2e-test.sh
```

### D1 — Terraform

```bash
cd infra/terraform
terraform init
terraform validate
terraform plan
```

### D4 — Kubernetes

```bash
cd infra/kubernetes
kubectl apply --dry-run=client -f .
```

### D6 — Observability

```bash
cd observability
docker compose up --build
./scripts/load-test.sh
```

## CI (D3)

GitHub Actions workflow at `.github/workflows/ci.yml` lints, tests, and builds container images on every push.

## License

MIT
