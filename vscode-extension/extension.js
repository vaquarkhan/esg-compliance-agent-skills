const vscode = require("vscode");
const path = require("path");
const fs = require("fs");

function repoRoot() {
  return path.resolve(__dirname, "..");
}

async function installFullToolkit() {
  const root = repoRoot();
  vscode.window.showInformationMessage(
    `ESG toolkit root: ${root}. Copy skills/, .cursor/rules/, and mcp/esg-mcp-servers.mcp.json per docs/cursor-setup.md`
  );
}

async function installMcpConfig() {
  const src = path.join(repoRoot(), "mcp", "esg-mcp-servers.mcp.json");
  const dest = path.join(
    repoRoot(),
    ".vscode",
    "mcp.json"
  );
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
  vscode.window.showInformationMessage(`Copied MCP config to ${dest}`);
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("esgAgentSkills.installFullToolkit", installFullToolkit),
    vscode.commands.registerCommand("esgAgentSkills.installMcpConfig", installMcpConfig)
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
