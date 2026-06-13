# Bootstrap ESG compliance agent skills (Windows)
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
Write-Host "ESG compliance agent skills bootstrapped."
