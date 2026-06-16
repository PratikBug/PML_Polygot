"""Tests demonstrating I6 seeded bug reproduction."""

from app.balance_bug import calculate_balance_buggy


def test_buggy_balance_fails_on_debit():
    """Reproduces I6 bug: debit transactions are ignored due to case mismatch."""
    txs = [
        {"amount": 100.0, "type": "credit"},
        {"amount": 30.0, "type": "debit"},
    ]
    balance = calculate_balance_buggy(txs)
    # Bug: returns 100 instead of 70 because "debit" != "DEBIT"
    assert balance == 100.0  # demonstrates the bug


def test_correct_balance_calculation():
    """Fixed version: normalize type to lowercase."""
    txs = [
        {"amount": 100.0, "type": "credit"},
        {"amount": 30.0, "type": "debit"},
    ]
    balance = 0.0
    for tx in txs:
        t = tx["type"].lower()
        if t == "credit":
            balance += tx["amount"]
        elif t == "debit":
            balance -= tx["amount"]
    assert balance == 70.0
