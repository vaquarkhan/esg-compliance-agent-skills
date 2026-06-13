Validate build artifacts and attestation envelopes.

Run: `python -m scripts.lifecycle.validate`

Writes `artifacts/validation_report.json`. Fails if any artifact missing `assurance_status: pending_sustainability_assurance_sign_off`.

Schema: `knowledge_base/attestation_schema.json`
