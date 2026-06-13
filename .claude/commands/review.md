SME and sustainability assuror review gate. Human reviewer must sign off before `/ship`.

Run: `python -m scripts.lifecycle.review --reviewer "Name"`

Writes `artifacts/review_record.json` with `outcome: pending` and `assurance_status: pending_sustainability_assurance_sign_off`.

Only a qualified sustainability assuror may set `sustainability_assurance_signed_off`. See `reviews/TEMPLATE.md`.
