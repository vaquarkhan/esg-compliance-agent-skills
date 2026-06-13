# Bootstrap ESG compliance agent skills (Windows)
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements-lock.txt -r requirements-dev.txt
python scripts/smoke_syntax.py
python scripts/validate-skills.py
Write-Host "ESG compliance agent skills bootstrapped. Run: make e2e"
