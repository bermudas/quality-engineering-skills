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

Then make sure Claude Code sees those variables when it starts. The simplest pattern is to source `.env` before launching:

```bash
set -a; source .env; set +a
claude
```

`.mcp.json` substitutes `${ELITEA_PROJECT_ID}` and `${ELITEA_TOKEN}` from the process environment at MCP server startup.

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
