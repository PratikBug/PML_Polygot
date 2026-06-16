# B3 — Test Discovery and Execution

**Target:** `services/transaction-api-python`

## Test Framework & Config

| Item | Value |
|------|-------|
| Framework | **pytest** |
| Config file | None (default pytest discovery) |
| Test directory | `tests/` |
| Dependencies | `pytest==8.3.4`, `httpx==0.28.1` in `requirements.txt` |

## Relevant Test Files

| File | Covers |
|------|--------|
| `tests/test_main.py` | All API endpoints, validation, balance calculation |
| `tests/test_bug_reproduction.py` | I6 seeded bug reproduction and fix verification |

## Exact Commands

```bash
cd services/transaction-api-python
pip install -r requirements.txt
pytest -v
```

## Actual Command Result

```
tests/test_main.py::test_health PASSED
tests/test_main.py::test_create_credit_transaction PASSED
tests/test_main.py::test_create_debit_transaction PASSED
tests/test_main.py::test_list_transactions PASSED
tests/test_main.py::test_balance_calculation PASSED
tests/test_main.py::test_validation_rejects_negative_amount PASSED
tests/test_main.py::test_validation_rejects_invalid_type PASSED
tests/test_bug_reproduction.py::test_buggy_balance_fails_on_debit PASSED
tests/test_bug_reproduction.py::test_correct_balance_calculation PASSED

9 passed
```

## Failure Interpretation

No failures in the main test suite. The `test_buggy_balance_fails_on_debit` test intentionally demonstrates the I6 seeded bug (balance returns 100 instead of 70 when debits use lowercase `"debit"` but the buggy code checks for `"DEBIT"`).

## All-Services Test Command

```bash
make test
```

Runs pytest, node --test, and cargo test across all services.
