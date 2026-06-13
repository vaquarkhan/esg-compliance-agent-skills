# Lifecycle artifacts (generated)

Run the full end-to-end pipeline:

```bash
make e2e
# or: python scripts/e2e_pipeline.py
```

Outputs (gitignored except this README):

| File | Lifecycle phase |
| --- | --- |
| `scope.json` | `/spec` |
| `plan.md`, `plan.json` | `/plan` |
| `build/*.json` | `/build` |
| `validation_report.json` | `/validate` |
| `review_record.json` | `/review` |
| `filing_package.json` | `/ship` |

All JSON artifacts carry `assurance_status: pending_sustainability_assurance_sign_off`.
