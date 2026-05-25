# elitea-next

Connect Claude Code to an EPAM **ELITEA Next** project over SSE.

The `.mcp.json` references two environment variables, so the same plugin works across multiple ELITEA projects and tenants without editing config:

| Variable | Source | Example |
| --- | --- | --- |
| `ELITEA_PROJECT_ID` | The numeric id in your ELITEA URL `https://next.elitea.ai/app/<ID>/sse` | `15742` |
| `ELITEA_TOKEN` | Personal access token, generated in ELITEA → Profile → API Tokens | `eyJ...` |

## Install

```bash
/plugin install elitea-next@quality-engineering-skills
```

## Configure

Copy `.env.example` to `.env` in your project root and fill in the two values:

```bash
cp .env.example .env
$EDITOR .env
```

That's it — no need to `source` anything. The plugin's `.mcp.json` runs a small `sh -c` wrapper that:

1. `grep`s `ELITEA_PROJECT_ID` and `ELITEA_TOKEN` out of `./.env` (the project root where you launch Claude Code),
2. Substitutes them into the ELITEA URL and `Authorization: Bearer` header,
3. Bridges the SSE endpoint to stdio via [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) so Claude Code can talk to it.

This is the same `.env`-reading pattern used elsewhere in this marketplace (e.g. the mobitru entries in [`NoMyGov`](https://github.com/bermudas)).

## Verify

Inside Claude Code:

```
/mcp
```

You should see `elitea-next` listed and connected. Try a quick tool call to confirm the bearer token is accepted (a 401 here means the token or project id is wrong).

## Notes

- The URL host (`next.elitea.ai`) is the SaaS instance. If you're on a self-hosted ELITEA, swap the host in `.mcp.json` — only the project id varies between projects on the same host.
- Tokens are project-scoped; rotate by replacing the value in `.env`.
- This plugin only ships the MCP wiring. Skills and agents that drive ELITEA workflows live in your project's own `.claude/` or in companion plugins.
