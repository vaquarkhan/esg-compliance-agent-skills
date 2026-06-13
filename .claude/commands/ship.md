Package filing artifacts for human-approved submission only.

Run: `python -m scripts.lifecycle.ship --human-approval-token PENDING`

Writes `artifacts/filing_package.json` with SHA-256 manifest. Calls `submit_csrd_filing` MCP stub — **rejects** until valid `human_approval_token`.

Never set assurance to signed-off without external sustainability assurance.
