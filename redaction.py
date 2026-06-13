"""ESG-oriented PII redaction gate before LLM reasoning.

Strips personal identifiers (names, national IDs, account numbers, email, phone)
from user text. Reversible tokens support authorized downstream deanonymization.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Pattern

# Patterns aligned with Skill 10 cross-border / AGENTS.md PII blocking rules.
EMAIL_RE: Pattern[str] = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE: Pattern[str] = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}\b")
SSN_RE: Pattern[str] = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
IBAN_RE: Pattern[str] = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
NATIONAL_ID_RE: Pattern[str] = re.compile(r"\b(?:PAN|Aadhaar|NIK|ID)[:\s#-]*[A-Z0-9-]{8,16}\b", re.I)
ACCOUNT_RE: Pattern[str] = re.compile(r"\b(?:account|acct)[:\s#-]*\d{6,16}\b", re.I)

PATTERN_MAP: list[tuple[str, Pattern[str]]] = [
    ("EMAIL", EMAIL_RE),
    ("PHONE", PHONE_RE),
    ("US_SSN", SSN_RE),
    ("IBAN", IBAN_RE),
    ("NATIONAL_ID", NATIONAL_ID_RE),
    ("ACCOUNT", ACCOUNT_RE),
]


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    entity_count: int
    entities_detected: list[str] = field(default_factory=list)


class ESGPIIRedactor:
    """Detect and mask PII with reversible token placeholders."""

    def __init__(self) -> None:
        self._token_counters: dict[str, int] = {}
        self._token_to_value: dict[str, str] = {}

    def reset_session(self) -> None:
        self._token_counters.clear()
        self._token_to_value.clear()

    def _next_token(self, entity_type: str, original_value: str) -> str:
        self._token_counters[entity_type] = self._token_counters.get(entity_type, 0) + 1
        token = f"<{entity_type}_{self._token_counters[entity_type]}>"
        self._token_to_value[token] = original_value
        return token

    def redact(self, text: str) -> RedactionResult:
        if not text.strip():
            return RedactionResult(original_text=text, redacted_text=text, entity_count=0)

        redacted = text
        entities: set[str] = set()
        count = 0

        for entity_type, pattern in PATTERN_MAP:
            matches = list(pattern.finditer(redacted))
            if not matches:
                continue
            entities.add(entity_type)
            for match in reversed(matches):
                value = match.group(0)
                token = self._next_token(entity_type, value)
                redacted = redacted[: match.start()] + token + redacted[match.end() :]
                count += 1

        return RedactionResult(
            original_text=text,
            redacted_text=redacted,
            entity_count=count,
            entities_detected=sorted(entities),
        )

    def deanonymize(self, text: str) -> str:
        restored = text
        for token in sorted(self._token_to_value, key=len, reverse=True):
            restored = restored.replace(token, self._token_to_value[token])
        return restored

    @property
    def active_token_count(self) -> int:
        return len(self._token_to_value)


def redact_text(text: str, *, redactor: ESGPIIRedactor | None = None) -> tuple[str, ESGPIIRedactor]:
    engine = redactor or ESGPIIRedactor()
    result = engine.redact(text)
    return result.redacted_text, engine
