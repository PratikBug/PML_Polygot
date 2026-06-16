#!/usr/bin/env bash
# D6 — Generate traffic for observability stack
set -euo pipefail

API_URL="${API_URL:-http://localhost:8090}"

echo "Generating traffic to $API_URL..."
for i in $(seq 1 20); do
  TYPE=$([ $((i % 2)) -eq 0 ] && echo "credit" || echo "debit")
  curl -sf -X POST "$API_URL/transactions" \
    -H "Content-Type: application/json" \
    -d "{\"amount\": $((RANDOM % 500 + 10)), \"type\": \"$TYPE\"}" > /dev/null
  curl -sf "$API_URL/health" > /dev/null
  curl -sf "$API_URL/metrics" > /dev/null
done

echo "Metrics snapshot:"
curl -sf "$API_URL/metrics" | python3 -m json.tool
