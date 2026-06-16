#!/usr/bin/env bash
# D2 — End-to-end test script for fraud-score docker-compose stack
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_DIR="$(dirname "$SCRIPT_DIR")"
API_URL="http://localhost:8002"

echo "==> Building and starting stack..."
cd "$COMPOSE_DIR"
docker compose up --build -d db api worker

echo "==> Waiting for API health..."
for i in $(seq 1 30); do
  if curl -sf "$API_URL/health" > /dev/null 2>&1; then
    echo "API is healthy"
    break
  fi
  sleep 2
done

echo "==> Submitting test transaction..."
RESP=$(curl -sf -X POST "$API_URL/transactions" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"e2e-user","amount":1500,"merchant":"Crypto Exchange","currency":"EUR"}')
TX_ID=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Created transaction ID: $TX_ID"

echo "==> Waiting for worker to score..."
for i in $(seq 1 20); do
  SCORE=$(curl -sf "$API_URL/transactions/$TX_ID/score" 2>/dev/null || echo "")
  if echo "$SCORE" | grep -q "risk_score"; then
    echo "Score received: $SCORE"
    break
  fi
  sleep 3
done

echo "==> Verifying score..."
SCORE=$(curl -sf "$API_URL/transactions/$TX_ID/score")
echo "$SCORE" | python3 -c "
import sys, json
s = json.load(sys.stdin)
assert s['risk_level'] == 'high', f'Expected high risk, got {s[\"risk_level\"]}'
assert s['risk_score'] >= 60, f'Expected score >= 60, got {s[\"risk_score\"]}'
print('E2E PASSED: risk_level=%s risk_score=%s' % (s['risk_level'], s['risk_score']))
"

echo "==> Checking worker logs..."
docker compose logs worker --tail=5

echo "==> All E2E tests passed!"
