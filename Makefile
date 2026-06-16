.PHONY: bootstrap test test-python test-node test-rust e2e docker-build lint clean

bootstrap:
	@echo "==> Bootstrapping Python services..."
	pip install -r services/transaction-api-python/requirements.txt
	pip install -r services/currency-converter/api/requirements.txt
	pip install -r systems/fraud-score/api/requirements.txt
	@echo "==> Bootstrapping Node services..."
	cd services/transaction-api-node && npm install
	cd services/currency-converter/client && npm install
	cd systems/fraud-score/worker && npm install
	@echo "==> Bootstrapping Rust projects..."
	cd services/log-counter-rust && cargo build
	cd systems/fraud-score/scorer && cargo build
	@echo "==> Bootstrap complete."

test: test-python test-node test-rust

test-python:
	cd services/transaction-api-python && pytest -v
	cd services/currency-converter/api && pytest -v
	cd systems/fraud-score/api && pytest -v

test-node:
	cd services/transaction-api-node && npm test
	cd services/currency-converter/client && npm test
	cd systems/fraud-score/worker && npm test

test-rust:
	cd services/log-counter-rust && cargo test
	cd systems/fraud-score/scorer && cargo test

e2e:
	cd systems/fraud-score && ./scripts/e2e-test.sh

docker-build:
	docker build -t transaction-api-python services/transaction-api-python
	docker build -t transaction-api-node services/transaction-api-node

lint:
	cd services/transaction-api-python && python -m py_compile app/main.py
	cd services/transaction-api-node && npm run lint 2>/dev/null || true

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
