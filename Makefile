.PHONY: install test lint validate mcp-local cdk-synth

install:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v

lint:
	ruff check .

validate:
	python scripts/validate-skills.py

mcp-local:
	python -m mcp.regulatory-db-server.server & \
	python -m mcp.emissions-factor-server.server

cdk-synth:
	cd infrastructure && cdk synth
