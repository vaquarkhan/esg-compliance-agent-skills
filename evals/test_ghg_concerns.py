"""Eval benchmark: GHG skill concern checklist."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GHG_SKILL = ROOT / "skills" / "ghg-emissions-calculation" / "SKILL.md"


def test_ghg_skill_cites_provenance():
    text = GHG_SKILL.read_text(encoding="utf-8")
    assert "factor_provenance.json" in text
    assert "get_emission_factor" in text


def test_ghg_skill_enforces_human_gate():
    text = GHG_SKILL.read_text(encoding="utf-8")
    assert "Human-in-the-loop" in text or "human review" in text.lower()
    assert "/review" in text or "sign-off" in text.lower()


def test_ghg_skill_scope2_dual_method():
    text = GHG_SKILL.read_text(encoding="utf-8")
    assert "location-based" in text.lower()
    assert "market-based" in text.lower()


def test_ghg_skill_forbids_invented_targets():
    text = GHG_SKILL.read_text(encoding="utf-8")
    assert "never invent" in text.lower() or "do not invent" in text.lower()
    assert "SBTi" in text
