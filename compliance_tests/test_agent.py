"""Agent entry smoke tests (TestModel when no API key)."""

from unittest.mock import AsyncMock, patch

import agent
from agent import ESGDeps, run_esg_agent_sync


def test_agent_module_exports():
    assert hasattr(agent, "run_esg_agent_sync")
    assert hasattr(agent, "esg_agent")


def test_run_agent_without_api_key():
    mock_result = AsyncMock()
    mock_result.output = "CSRD double materiality requires impact and financial axes."
    with patch.object(agent.esg_agent, "run", return_value=mock_result):
        output = run_esg_agent_sync("Summarize CSRD double materiality steps.")
    assert isinstance(output, str)
    assert len(output) > 0


def test_redaction_before_agent():
    deps = ESGDeps()
    mock_result = AsyncMock()
    mock_result.output = "Emissions review complete."
    with patch.object(agent.esg_agent, "run", return_value=mock_result) as mock_run:
        output = run_esg_agent_sync(
            "Review emissions for contact ops@example.com",
            deps=deps,
        )
    assert "ops@example.com" not in output
    assert deps.last_redaction is not None
    assert deps.last_redaction.entity_count >= 1
    redacted_prompt = mock_run.call_args[0][0]
    assert "ops@example.com" not in redacted_prompt
