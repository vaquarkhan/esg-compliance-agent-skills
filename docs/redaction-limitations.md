# Redaction limitations

The PII redaction gate (`redaction.py`) uses **regex-based** detection for common ESG workflow identifiers. Understand limits before production use.

## Coverage

| Detected | Not detected by default |
| --- | --- |
| Email, phone, US SSN | Non-English names without Latin script |
| IBAN, labeled national IDs | Unlabeled free-text personal names |
| Labeled account numbers | OCR-degraded scans |

## Recommendations

1. Extend `PATTERN_MAP` for jurisdiction-specific IDs (Aadhaar, NIN, etc.)
2. Integrate Microsoft Presidio for clinical/financial free text if needed
3. Route India/China/Saudi data through Skill 10 before persistence
4. Human review before external disclosure

## Related

- [Architecture](architecture.md)
- Skill `cross-border-data-transfer`
