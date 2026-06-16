"""BUG SEED for I6 — balance calculation fails for debit transactions.

Root cause: case-sensitive comparison 'DEBIT' vs normalized 'debit'.
Fix: compare lowercase type values consistently.
"""

def calculate_balance_buggy(transactions):
    balance = 0.0
    for tx in transactions:
        if tx["type"] == "credit":
            balance += tx["amount"]
        elif tx["type"] == "DEBIT":  # BUG: incoming type is lowercase "debit"
            balance -= tx["amount"]
    return balance
