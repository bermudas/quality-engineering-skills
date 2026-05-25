# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal Claude Code plugin marketplace (`quality-engineering-skills`) curated by @bermudas, focused on QE / test automation / SDLC tooling. Distributed via `/plugin marketplace add bermudas/quality-engineering-skills`. Ships ~40 plugins: in-repo wrappers, vendored skills, and mirrored entries from upstream marketplaces (sdlc-skills, servicenow-atf-skill).

## The generator pattern (read this first)

`.claude-plugin/marketplace.json` is **generated**. Hand-editing it will fail CI (`build-check.yml` runs the generator and diffs).

- **Source of truth:** [`scripts/marketplace-sources.json`](scripts/marketplace-sources.json)
- **Generator:** [`scripts/build-marketplace.py`](scripts/build-marketplace.py) — stdlib-only, no deps
- **After any edit:** `python3 scripts/build-marketplace.py && claude plugin validate .`

The Claude Code marketplace schema has no `import`/`include` syntax — every plugin must be its own `source` block. The generator works around this by fetching each upstream marketplace's `.claude-plugin/marketplace.json` at the pinned SHA and inlining every entry as a `git-subdir` or `url` source. This is what enables drill-down install (e.g., `/plugin install code-review@quality-engineering-skills` lands one skill out of sdlc-skills' 30).

Fields the schema doesn't recognize (notably the `upstream` tracking block on `local_plugins`) are stripped by the generator before writing the output. They live in the sources file as documentation but never reach the published marketplace.

## Common commands

```bash
# Regenerate marketplace.json from sources
python3 scripts/build-marketplace.py

# Validate the marketplace + every in-repo plugin manifest
claude plugin validate .

# Lint YAML frontmatter on every SKILL.md / agents/*.md / commands/*.md
python3 .github/scripts/validate_frontmatter.py

# Dry-run the nightly SHA-bump locally (uses gh CLI for auth)
GH_TOKEN=$(gh auth token) python3 .github/scripts/bump_upstreams.py

# Refresh the vendored agent-evaluator skill from upstream at a specific sha
SHA=<commit-sha> external_plugins/agent-evaluator/scripts/vendor-from-upstream.sh

# Manually trigger the nightly bump on GitHub
gh workflow run "Bump Upstream SHAs"
```

There are no tests in this repo. CI is the test harness — `validate-plugins`, `build-check`, `validate-frontmatter` all run on every PR.

## Three classes of plugins under `external_plugins/`

Don't mix these up — each has a different anatomy:

1. **Real MCP plugins** (e.g. `elitea-next`). Carry `.mcp.json` + `.env.example`. Doing actual work — installing the plugin wires up an MCP server. See [the elitea-next gotcha](#elitea-next-mcp-config-gotcha) below.
2. **Vendored skills** (e.g. `agent-evaluator`). The upstream skill files are copied into `skills/<name>/` and pinned to a specific SHA in `scripts/marketplace-sources.json`. A `scripts/vendor-from-upstream.sh` script refreshes them.
3. **Thin wrappers** (e.g. `qa-agent`, `qaspace-skill`, `qavajs-skill`, `vividus-skill`, `tosca-tsu`, `toscacloud-cli`). Plugin manifest + README only, no actual asset directories. The README points at the upstream `npx … init` installer. These exist so the marketplace can advertise them; installing the wrapper alone does almost nothing — the user still runs the upstream installer.

When adding a new plugin, decide which class first.

## Adding a new plugin — the four routes

### A. New in-repo plugin (you're authoring it here)

```bash
cp -R plugins/example-plugin plugins/your-plugin
$EDITOR plugins/your-plugin/.claude-plugin/plugin.json
```

Then add an entry to `scripts/marketplace-sources.json` under `local_plugins`, pointing `source` at `./plugins/your-plugin`. Regenerate, validate, PR.

### B. Wrapper around an upstream npx skill bundle

The bundle's repo doesn't follow Claude Code plugin format (no `.claude-plugin/plugin.json` upstream). Create `external_plugins/<name>/` with just `.claude-plugin/plugin.json` + `README.md` pointing at the upstream `npx … init` command. Pin the upstream SHA in the `upstream` block in `marketplace-sources.json` (purely for tracking and auto-bump — it's stripped from the output).

### C. Vendor a skill from a third-party `skills/` repo

If the upstream is a `.claude/skills/<thing>` folder in someone else's repo (like `dshaplyko/skills`), create `external_plugins/<name>/skills/<thing>/` and copy `SKILL.md` + references. Write a `scripts/vendor-from-upstream.sh` that does the copy from a pinned SHA so refreshes are deterministic. Pattern: see `external_plugins/agent-evaluator/`.

### D. Mirror an entire upstream marketplace (drill-down install)

If the upstream repo already has a `.claude-plugin/marketplace.json` (arozumenko/sdlc-skills, bermudas/servicenow-atf-skill), don't wrap anything in-repo. Add a new block to `upstream_marketplaces` in `scripts/marketplace-sources.json`:

```json
{
  "url": "https://github.com/owner/repo.git",
  "ref": "main",
  "sha": "<full-sha>",
  "include": ["*"],
  "default_category": "testing",
  "category_overrides": { "specific-name": "planning" },
  "author": {"name": "...", "url": "..."}
}
```

`include` filters by plugin name (`["*"]` keeps all). `category_overrides` lets you re-bucket individual sub-plugins. The generator handles everything else — runs `python3 scripts/build-marketplace.py` and the entries appear.

## elitea-next MCP config gotcha

The current `.mcp.json` looks unusual on purpose. Three constraints drove its shape:

```json
{
  "elitea-next": {
    "type": "sse",
    "url": "https://next.elitea.ai/app/${ELITEA_PROJECT_ID}/sse",
    "headersHelper": "printf '{\"Authorization\":\"Bearer %s\"}' $(grep -m1 '^ELITEA_TOKEN=' .env | cut -d= -f2-)",
    "env": { "ELITEA_PROJECT_ID": "15742" }
  }
}
```

1. **`url` only supports `${VAR}` substitution from process env, not shell command substitution and not `.env` reading.** That's why `ELITEA_PROJECT_ID` has to live in process env (or be defaulted via the server-scoped `env` block — which works on this SSE server in practice even though the docs describe `env` for stdio's spawned process).
2. **`headersHelper` IS a documented Claude Code field** (see [docs](https://code.claude.com/docs/en/mcp#use-dynamic-headers-for-custom-authentication)). It runs an arbitrary shell command on each connect and merges its JSON-object stdout into request headers. That's the only way to get `.env` reading into header values — `url` and `env` can't do shell substitution.
3. **`mcp-remote` as a stdio bridge was tried and rejected.** The user prefers the native SSE shape. Don't revert without checking.

If asked to "add an MCP that reads from `.env`": use the same shape. Token-in-`.env` → `headersHelper`. Numeric/static-ish config → server-scoped `env` block with a default + process-env override.

## CI workflows (`.github/workflows/`)

| Workflow | Trigger | Notes |
| --- | --- | --- |
| `validate-plugins.yml` | PR + push (paths-filtered) | Uses `anthropics/claude-plugins-community/.github/actions/validate-plugins@<sha>` — SHA-pinned. |
| `build-check.yml` | PR + push | Regenerates `marketplace.json`, fails if drifted. **This is why hand-edits to the output get rejected.** |
| `validate-frontmatter.yml` | PR + push | Python stdlib + PyYAML. Checks `name` + `description` on every skill/agent/command markdown. |
| `bump-upstreams.yml` | Cron `0 6 * * *` UTC + manual dispatch | Polls GitHub API for moved SHAs, bumps `marketplace-sources.json`, regenerates, validates inline, opens PR, squash-merges immediately. Force-resets the `bump/upstream-shas` branch each run. |

The bump workflow needs two repo settings flipped (one-time): **Settings → Actions → General** → "Read and write permissions" + "Allow GitHub Actions to create and approve pull requests". Without these, `gh pr create` returns 403.

## Conventions

- Plugin names: kebab-case, no underscores, no namespacing prefix. Generic names like `code-review` and `memory` collide with other marketplaces by topic but not by identifier (`@quality-engineering-skills` scopes them) — don't rename to avoid imagined collisions.
- Pin upstream SHAs everywhere a `url` is referenced. The bump workflow keeps them current.
- Wrapper plugins should be honest in their README that they're pointer-installers — installing the wrapper alone doesn't install upstream skill files.
- Don't add `version` fields to plugin entries unless you commit to maintaining them; the marketplace works fine without (Claude Code falls back to commit SHA).
- Never add fields to `marketplace.json` entries that aren't in the documented schema (`name`, `description`, `author`, `source`, `category`, `tags`, `strict`, `homepage` + manifest fields). `claude plugin validate` warns on unknown fields. The generator strips `upstream` for this reason — keep documentation-only fields in `marketplace-sources.json`, not the output.
