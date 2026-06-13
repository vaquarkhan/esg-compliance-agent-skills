#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-lock.txt -r requirements-dev.txt
python scripts/smoke_syntax.py
python scripts/validate-skills.py
echo "ESG compliance agent skills bootstrapped. Run: make e2e"
