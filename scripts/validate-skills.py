#!/usr/bin/env python3
"""Validate all SKILL.md files have required YAML frontmatter."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
pattern = re.compile(r"^---\nname: .+\ndescription: .+\n---", re.MULTILINE)
errors = []
for skill_md in SKILLS.glob("*/SKILL.md"):
    text = skill_md.read_text(encoding="utf-8")
    if not pattern.search(text):
        errors.append(str(skill_md))
if errors:
    print("Invalid SKILL.md frontmatter:", *errors, sep="\n")
    sys.exit(1)
print(f"Validated {len(list(SKILLS.glob('*/SKILL.md')))} skills.")
