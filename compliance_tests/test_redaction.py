"""PII redaction tests."""

from redaction import ESGPIIRedactor, redact_text


def test_redact_email():
    redactor = ESGPIIRedactor()
    result = redactor.redact("Contact analyst@example.com for CSRD data.")
    assert "analyst@example.com" not in result.redacted_text
    assert "<EMAIL_1>" in result.redacted_text
    assert result.entity_count == 1


def test_deanonymize_restores_tokens():
    redactor = ESGPIIRedactor()
    original = "Reviewer jane.doe@corp.eu signed off."
    result = redactor.redact(original)
    restored = redactor.deanonymize(result.redacted_text)
    assert "jane.doe@corp.eu" in restored


def test_redact_text_helper():
    redacted, engine = redact_text("Account: acct 123456789012")
    assert "123456789012" not in redacted
    assert engine.active_token_count >= 1
