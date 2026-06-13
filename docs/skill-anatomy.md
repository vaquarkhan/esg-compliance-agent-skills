# Skill anatomy

Each skill lives in `skills/<name>/SKILL.md` with:

```yaml
---
name: skill-name
description: Third-person description with trigger terms
---
```

## Required sections

1. Scope
2. Mandatory constraints (human-in-the-loop, no guessing)
3. Workflow steps
4. MCP tools
5. Output artifacts
6. Anti-patterns

Validate with `python scripts/validate-skills.py`.
