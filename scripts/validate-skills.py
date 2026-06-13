#!/usr/bin/env python3
"""Validate SKILL.md files: frontmatter, structure, naming, and headings."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

FRONTMATTER_RE = re.compile(
    r"^---\nname: (?P<name>.+)\ndescription: (?P<desc>.+)\n---",
    re.MULTILINE,
)

REQUIRED_SECTIONS = [
    "Mandatory constraints",
]

ANTI_PATTERN_SECTIONS = ["Anti-patterns", "Common rationalizations", "Red flags"]

RECOMMENDED_SECTIONS = [
    "Overview",
    "When to Use",
    "Verification",
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    folder_name = path.parent.name

    fm = FRONTMATTER_RE.search(text)
    if not fm:
        errors.append(f"{path}: missing or invalid YAML frontmatter (name + description required)")
        return errors

    name = fm.group("name").strip()
    if name != folder_name:
        errors.append(f"{path}: frontmatter name '{name}' != folder '{folder_name}'")

    if len(fm.group("desc").strip()) < 40:
        errors.append(f"{path}: description too short (< 40 chars) — add trigger terms")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path}: missing required section '{section}'")

    if not any(section in text for section in ANTI_PATTERN_SECTIONS):
        errors.append(f"{path}: missing anti-pattern section (one of {ANTI_PATTERN_SECTIONS})")

    body_lines = len(text.splitlines())
    min_lines = 70 if folder_name != "using-esg-agent-skills" else 45
    if body_lines < min_lines:
        errors.append(f"{path}: body too short ({body_lines} lines, min {min_lines})")

    headings = [m.group(2).strip().lower() for m in HEADING_RE.finditer(text)]
    seen: set[str] = set()
    for h in headings:
        if h in seen:
            errors.append(f"{path}: duplicate heading '{h}'")
        seen.add(h)

    if "Human-in-the-loop" not in text and "human" not in text.lower():
        errors.append(f"{path}: must mention human-in-the-loop or human review gate")

    if "No guessing" not in text and "never invent" not in text.lower():
        errors.append(f"{path}: must forbid guessing/inventing regulatory or factor data")

    if "Verification checklist" not in text and "Verification" not in text:
        errors.append(f"{path}: missing verification checklist section")

    return errors


def main() -> int:
    if not SKILLS.exists():
        print(f"ERROR: {SKILLS} not found", file=sys.stderr)
        return 1

    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if not skill_files:
        print("ERROR: no skills found", file=sys.stderr)
        return 1

    domain_skills = {
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
    }
    found_domain = {p.parent.name for p in skill_files}
    missing_domain = domain_skills - found_domain

    all_errors: list[str] = []
    if missing_domain:
        all_errors.append(f"Missing domain skills: {sorted(missing_domain)}")

    for skill_md in skill_files:
        all_errors.extend(validate_skill(skill_md))

    if all_errors:
        print("Skill validation failed:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(skill_files)} skills "
        f"({len(domain_skills)} domain + meta); frontmatter, sections, names, headings OK."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
