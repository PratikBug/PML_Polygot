# D6 — Observability Stack

Prometheus + Grafana monitoring for the observable transaction API.

## Run Order

```bash
docker compose up --build
./scripts/load-test.sh
```

- API: http://localhost:8090
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

## Metrics Endpoint

```bash
curl http://localhost:8090/metrics
```

Returns JSON metrics: `transaction_total`, `http_requests_total`, `balance_current`, etc.
