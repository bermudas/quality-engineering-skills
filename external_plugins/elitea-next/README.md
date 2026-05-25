# elitea-next

Connect Claude Code to an EPAM **ELITEA Next** project over SSE.

The `.mcp.json` references two values:

| Value | Where it comes from | Default |
| --- | --- | --- |
| `ELITEA_PROJECT_ID` | Server-scoped `env` block in `.mcp.json` (defaults to `15742`). Override by editing `.mcp.json` or by exporting `ELITEA_PROJECT_ID` in your shell — process env wins if set. | `15742` |
| `ELITEA_TOKEN` | Read from `.env` at connect time by `headersHelper` (a documented Claude Code field that runs a shell command and merges JSON stdout into headers). | none — required |

## Install

```bash
/plugin install elitea-next@quality-engineering-skills
```

## Configure

Copy `.env.example` to `.env` in your project root and drop in your token:

```bash
cp .env.example .env
$EDITOR .env   # set ELITEA_TOKEN
```

That's it — `.env` only needs `ELITEA_TOKEN`. The project id defaults to `15742` (set in the `env` block inside `.mcp.json`). To point at a different project, either edit that block in `.mcp.json` or export the var in your shell before launching Claude Code:

```bash
export ELITEA_PROJECT_ID=12345
claude
```

### Why ELITEA_PROJECT_ID isn't in `.env`

Claude Code's `.mcp.json` semantics differ by field:

- **`headersHelper`** runs an arbitrary shell command and merges its JSON stdout into request headers, so it can `grep .env` for the token directly.
- **`url`** only supports `${VAR}` / `${VAR:-default}` substitution from process env — no shell substitution, no `.env` reading.

So the token comes from `.env` (via `headersHelper`), and the project id comes from process env with a baked-in default. Putting `ELITEA_PROJECT_ID` in `.env` would have no effect.

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
