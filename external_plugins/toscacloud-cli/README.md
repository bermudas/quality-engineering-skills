# toscacloud-cli

Wrapper for [bermudas/toscacloud_cli](https://github.com/bermudas/toscacloud_cli) — an AI-native CLI for **Tricentis Tosca Cloud**, plus a Tosca Cloud MCP server.

## What it includes upstream

- `tosca_cli.py` — Python CLI for Tosca Cloud workspace operations.
- `.mcp.json` — Tosca Cloud MCP server (`mcp-remote` to `https://<tenant>.my.tricentis.com/<workspace>/_mcp/api/mcp`) + bundled Playwright MCP.
- `.claude/` — Claude Code skills that wrap the CLI for the agent.
- `CLAUDE.md` + `AGENTS.md` — operating guidance for agents.

## Install

1. Marketplace entry:

   ```bash
   /plugin install toscacloud-cli@quality-engineering-skills
   ```

2. Clone the upstream and set up locally — it expects a real `.env`:

   ```bash
   git clone https://github.com/bermudas/toscacloud_cli
   cd toscacloud_cli
   cp .env.example .env
   $EDITOR .env   # tenant, workspace id, credentials
   pip install -r requirements.txt
   ```

3. The bundled MCP URL in upstream's `.mcp.json` contains `<YourTenant>` and `<Workspaceid>` placeholders — replace them before launching Claude Code.

## Upstream

- Repo: <https://github.com/bermudas/toscacloud_cli>
- Tricentis Tosca Cloud: <https://www.tricentis.com/products/tosca-cloud>
- Pinned: see `sha` in the marketplace.json entry
