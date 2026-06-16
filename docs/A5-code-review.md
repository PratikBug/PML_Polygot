# A5 — Agent Code Review and Adversarial Verification

**Reviewed PR:** Hypothetical agent-generated PR adding bulk transaction import

## Issue List

| # | Issue | Severity | Blocking? | File |
|---|-------|----------|-----------|------|
| 1 | No input size limit on bulk import — DoS vector | Critical | Yes | `app/main.py` |
| 2 | SQL injection via unsanitized merchant field | Critical | Yes | `app/main.py` |
| 3 | Missing test for empty bulk import | Medium | No | `tests/` |
| 4 | Balance not recalculated atomically during bulk import | High | Yes | `app/main.py` |
| 5 | No authentication on POST endpoints | High | Yes | `app/main.py` |
| 6 | `amount` accepts float without decimal precision control | Medium | No | `app/main.py` |
| 7 | No request timeout middleware | Low | No | `app/main.py` |
| 8 | README not updated with new endpoint | Low | No | `README.md` |

## Suggested Fixes

| # | Fix |
|---|-----|
| 1 | Add `max_length=100` on bulk import list; reject >100 items |
| 2 | Use parameterized queries; Pydantic validation already helps but add `merchant` regex `^[a-zA-Z0-9 ]+$` |
| 3 | Add `test_bulk_import_empty_list` returning 400 |
| 4 | Wrap bulk import in transaction block; recalculate balance once at end |
| 5 | Add API key middleware (even simple header check for demo) |
| 6 | Use `Decimal` type or round to 2 decimal places |
| 7 | Add `timeout` middleware via starlette |
| 8 | Update README with bulk endpoint docs |

## Verification Steps

```bash
# Test size limit
curl -X POST /transactions/bulk -d '{"transactions": [<101 items>]}'  # expect 422

# Test SQL injection
curl -X POST /transactions -d '{"amount": 10, "type": "credit", "merchant": "'; DROP TABLE--"}'  # expect 422

# Run full test suite
pytest -v  # all must pass
```

## Classification Summary

- **Blocking (3):** Issues 1, 2, 4, 5 — must fix before merge
- **Non-blocking (4):** Issues 3, 6, 7, 8 — fix in follow-up
