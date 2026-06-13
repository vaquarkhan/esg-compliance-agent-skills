# Plugin publishing — VS Code & JetBrains

Manual publish steps for **ESG Compliance Agent Skills** v1.0.0+.

## Before you publish

1. Bump `VERSION` and run `make sync-version`
2. Validate: `make validate`
3. Build artifacts (below)
4. Tag: `git tag v1.0.0 && git push origin v1.0.0`
5. Create a [GitHub Release](https://github.com/vaquarkhan/esg-compliance-agent-skills/releases/new) and attach:
   - `vscode-extension/esg-compliance-agent-skills-1.0.0.vsix`
   - `jetbrains-plugin/build/distributions/*.zip`

## Build locally

### VS Code

```powershell
cd vscode-extension
npm install -g @vscode/vsce
vsce package --no-dependencies
```

### JetBrains

```powershell
cd jetbrains-plugin
.\gradlew.bat buildPlugin
```

Requires **JDK 17+**.

## GitHub release template

**Title:** `v1.0.0 - ESG agent ecosystem and IDE plugins`

**Summary:**

- CI: Ruff, mypy, pip-audit, Bandit, detect-secrets, CodeQL, pytest coverage (≥80% on agent.py + redaction.py)
- 10 ESG skills, 5 MCP SSE servers, AWS CDK stack
- IDE plugins: VS Code (.vsix) and JetBrains (.zip) attached

See [CHANGELOG.md](../CHANGELOG.md).
