#!/usr/bin/env bash
# I4 — Scripted end-to-end verification: API + Node CLI
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
API_DIR="$ROOT_DIR/api"
CLIENT_DIR="$ROOT_DIR/client"
PORT=8001
API_URL="http://localhost:$PORT"

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then
    kill "$API_PID" 2>/dev/null || true
    wait "$API_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "==> Installing API dependencies..."
pip3 install -q -r "$API_DIR/requirements.txt"

echo "==> Starting FastAPI on port $PORT..."
cd "$API_DIR"
python3 -m uvicorn app.main:app --port "$PORT" &
API_PID=$!

echo "==> Waiting for API health..."
for i in $(seq 1 20); do
  if curl -sf "$API_URL/health" > /dev/null 2>&1; then
    echo "API healthy"
    break
  fi
  sleep 0.5
done

echo "==> Running API unit tests..."
python3 -m pytest -v

echo "==> Running client unit tests..."
cd "$CLIENT_DIR"
npm test

echo "==> E2E: CLI converts USD → EUR..."
OUTPUT=$(CONVERTER_API_URL="$API_URL" node cli.js USD EUR 100)
echo "$OUTPUT"
echo "$OUTPUT" | grep -q "100 USD = 92 EUR"

echo "==> E2E: curl POST /convert..."
CURL_RESULT=$(curl -sf -X POST "$API_URL/convert" \
  -H "Content-Type: application/json" \
  -d '{"from_currency":"GBP","to_currency":"INR","amount":10}')
echo "$CURL_RESULT"
echo "$CURL_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['converted_amount'] > 0"

echo ""
echo "========================================="
echo "  I4 VERIFICATION PASSED — all green"
echo "========================================="
