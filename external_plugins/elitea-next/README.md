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

Copy `.env.example` to `.env` in your project root:

```bash
cp .env.example .env
$EDITOR .env
```

The two values are loaded differently because Claude Code's `.mcp.json` semantics are different for each field:

| Variable | How it's loaded | Why |
| --- | --- | --- |
| `ELITEA_TOKEN` | Read from `.env` at connect time by the `headersHelper` shell command. | `headersHelper` runs an arbitrary shell command whose JSON stdout is merged into request headers — so it can `grep .env` directly. |
| `ELITEA_PROJECT_ID` | Read from **process env** at MCP-server startup via `${ELITEA_PROJECT_ID}` substitution. | Claude Code only does `${VAR}` substitution in `url` (no shell substitution, no `.env` reading). |

So `ELITEA_PROJECT_ID` needs to be in the shell environment when you launch Claude Code. Pick one:

1. **direnv** — drop the same value into a `.envrc` (`export ELITEA_PROJECT_ID=15742`) and direnv auto-loads it when you `cd` into the project. Recommended if you already use direnv.
2. **Source `.env` once per shell** — `set -a; source .env; set +a; claude`.
3. **Export from your shell rc** — `export ELITEA_PROJECT_ID=15742` in `~/.zshrc` if you only ever use one project.

If `ELITEA_PROJECT_ID` is missing, Claude Code will fail to parse the MCP config and `/mcp` will show `elitea-next` as failed.

## Verify

Inside Claude Code:

```
/mcp
```

You should see `elitea-next` listed and connected. A 401 means the token in `.env` is wrong or missing; a 404 means the project id is wrong.

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
