"""Verify all 10 domain ESG skills + meta skill exist and meet content bar."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

DOMAIN_SKILLS = [
    "data-ingestion-validation",
    "ghg-emissions-calculation",
    "eu-taxonomy-alignment",
    "double-materiality-assessment",
    "sfdr-pai-computation",
    "audit-trail-reporting",
    "regulatory-change-monitor",
    "supply-chain-due-diligence",
    "biodiversity-tnfd-analytics",
    "cross-border-data-transfer",
]


def test_all_domain_skills_present():
    for name in DOMAIN_SKILLS:
        path = SKILLS / name / "SKILL.md"
        assert path.exists(), f"missing {path}"


def test_meta_skill_present():
    assert (SKILLS / "using-esg-agent-skills" / "SKILL.md").exists()


def test_each_skill_has_playbook_sections():
    required = ["Mandatory constraints", "Verification checklist"]
    anti = ["Common rationalizations", "Anti-patterns", "Red flags"]
    for name in DOMAIN_SKILLS + ["using-esg-agent-skills"]:
        text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
        for sec in required:
            assert sec in text, f"{name} missing {sec}"
        assert any(a in text for a in anti), f"{name} missing anti-pattern section"


def test_registry_matches_filesystem():
    import json

    manifest = json.loads((ROOT / "registry" / "skills.json").read_text(encoding="utf-8"))
    registered = {s["name"] for s in manifest["domain_skills"]}
    assert registered == set(DOMAIN_SKILLS)
