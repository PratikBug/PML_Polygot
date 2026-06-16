# I6 — Bug Diagnosis with Agent

**Repo:** `services/transaction-api-python`  
**Bug location:** `app/balance_bug.py`

## Reproduction Steps

1. Import the buggy balance function:
   ```bash
   cd services/transaction-api-python
   pytest tests/test_bug_reproduction.py::test_buggy_balance_fails_on_debit -v
   ```
2. Observe: balance is 100.0 instead of expected 70.0 after credit(100) + debit(30)

## Root Cause

**File:** `app/balance_bug.py`, line 12

```python
elif tx["type"] == "DEBIT":  # BUG: incoming type is lowercase "debit"
```

The API normalizes transaction types to lowercase (`"credit"`, `"debit"`) in `app/main.py` via the Pydantic validator. The buggy function compares against uppercase `"DEBIT"`, so debit transactions are silently ignored in balance calculation.

## Minimal Fix

```python
def calculate_balance_buggy(transactions):
    balance = 0.0
    for tx in transactions:
        t = tx["type"].lower()
        if t == "credit":
            balance += tx["amount"]
        elif t == "debit":
            balance -= tx["amount"]
    return balance
```

## Verification Command and Result

```bash
pytest tests/test_bug_reproduction.py::test_correct_balance_calculation -v
# PASSED — balance correctly returns 70.0
```

## Agent Suggested vs Manually Verified

| Item | Agent Suggested | Manually Verified |
|------|----------------|-------------------|
| Root cause is case sensitivity | Yes | Confirmed by reading `balance_bug.py` line 12 |
| Fix: normalize to lowercase | Yes | Ran fixed test, passes |
| Bug also in main.py | Agent incorrectly flagged | Verified `main.py` uses lowercase comparison correctly |
| Impact: all debit transactions | Yes | Confirmed via test with single debit |
