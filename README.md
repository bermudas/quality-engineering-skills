# Quality Engineering Skills

A Claude Code plugin marketplace focused on **quality engineering, test automation, and SDLC tooling**. Curated and maintained by [@bermudas](https://github.com/bermudas).

[![Validate Plugins](https://github.com/bermudas/quality-engineering-skills/actions/workflows/validate-plugins.yml/badge.svg)](https://github.com/bermudas/quality-engineering-skills/actions/workflows/validate-plugins.yml)
[![Build Check](https://github.com/bermudas/quality-engineering-skills/actions/workflows/build-check.yml/badge.svg)](https://github.com/bermudas/quality-engineering-skills/actions/workflows/build-check.yml)
[![Validate Frontmatter](https://github.com/bermudas/quality-engineering-skills/actions/workflows/validate-frontmatter.yml/badge.svg)](https://github.com/bermudas/quality-engineering-skills/actions/workflows/validate-frontmatter.yml)
[![Bump Upstream SHAs](https://github.com/bermudas/quality-engineering-skills/actions/workflows/bump-upstreams.yml/badge.svg)](https://github.com/bermudas/quality-engineering-skills/actions/workflows/bump-upstreams.yml)

> **⚠️ Trust before installing.** Plugins listed here run MCP servers and skills that may have access to your code, secrets, and external systems. Inspect each plugin's source before installing, updating, or using it.

## Install this marketplace

```text
# Inside Claude Code
/plugin marketplace add bermudas/quality-engineering-skills
/plugin install <plugin-name>@quality-engineering-skills
```

Or browse it interactively with `/plugin > Discover` after adding the marketplace.

## Repo layout

```
.
├── .claude-plugin/
│   └── marketplace.json          # generated — do not hand-edit
├── .github/
│   ├── workflows/                # validate-plugins, build-check, validate-frontmatter, bump-upstreams
│   └── scripts/                  # python helpers for the workflows
├── plugins/
│   └── example-plugin/           # template for new in-repo plugins
├── external_plugins/             # thin wrappers around upstream skill bundles + ELITEA MCP
└── scripts/
    ├── marketplace-sources.json  # source of truth — edit this
    └── build-marketplace.py      # regenerates .claude-plugin/marketplace.json from sources
```

## Featured plugins

The marketplace ships **~40 plugins**. The headliners:

| Plugin | Source | What it does |
| --- | --- | --- |
| [`elitea-next`](external_plugins/elitea-next) | in-repo (SSE MCP) | Connect Claude Code to an EPAM **ELITEA Next** project over SSE. Reads project id from a server-scoped `env` block and bearer token from `.env` via `headersHelper`. |
| [`qa-agent`](external_plugins/qa-agent) | wraps [onetest-ai/qa-agent](https://github.com/onetest-ai/qa-agent) | Multi-specialist QA agent — exploratory testing, accessibility, security, test generation, with a `/qa-init` onboarding pipeline. |
| [`agent-evaluator`](external_plugins/agent-evaluator) | vendors [dshaplyko/skills/.../agent-evaluator](https://github.com/dshaplyko/skills/tree/main/.claude/skills/agent-evaluator) | Score AI agent specifications against the Agent Maturity Model (L0–L3, 39 practices) and emit a styled HTML report. |
| `sdlc-skills` and 29 sub-plugins | mirrors [arozumenko/sdlc-skills](https://github.com/arozumenko/sdlc-skills) at a pinned SHA | Role-based agents (BA, Tech Lead, PM, Python/JS/iOS devs, QA, Test Automation Engineer) + workflow skills (`bugfix-workflow`, `plan-feature`, `code-review`, `git-workflow`, `playwright-testing`, …). Install the umbrella for everything, or pick one. |
| `servicenow-atf-automation` | mirrors [bermudas/servicenow-atf-skill](https://github.com/bermudas/servicenow-atf-skill) | ServiceNow ATF — Fluent SDK (`now-sdk build/install`) and a zero-install Scripted-REST builder for `glide_var` step inputs. |
| [`qaspace-skill`](external_plugins/qaspace-skill) | wraps [bermudas/qaspace-skill](https://github.com/bermudas/qaspace-skill) | Query EPAM **qaspace** Test Management Plugin on Jira Server/DC via JQL or MCP. |
| [`qavajs-skill`](external_plugins/qavajs-skill) | wraps [bermudas/qavajs-skill](https://github.com/bermudas/qavajs-skill) | qavajs BDD framework — 270 step patterns, full config and DSL reference. |
| [`vividus-skill`](external_plugins/vividus-skill) | wraps [bermudas/vividus-skill](https://github.com/bermudas/vividus-skill) | Vividus test automation framework — bootstrap, configure, author, run. |
| [`tosca-tsu`](external_plugins/tosca-tsu) | wraps [bermudas/ToscaTSU](https://github.com/bermudas/ToscaTSU) | Bidirectional bridge between Tricentis Tosca `.tsu` bundles and Playwright TypeScript specs. |
| [`toscacloud-cli`](external_plugins/toscacloud-cli) | wraps [bermudas/toscacloud_cli](https://github.com/bermudas/toscacloud_cli) | AI-native CLI for Tricentis Tosca Cloud. |

The complete list lives in [`scripts/marketplace-sources.json`](scripts/marketplace-sources.json) (source of truth) and [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) (generated).

## Plugin layout

Each plugin in this marketplace follows the standard Claude Code plugin layout:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata (required)
├── .mcp.json            # MCP server configuration (optional)
├── .env.example         # Required env vars (when a plugin reads them)
├── commands/            # Slash commands (optional)
├── agents/              # Agent definitions (optional)
├── skills/              # Skill definitions (optional)
└── README.md            # Documentation
```

Wrapper plugins under `/external_plugins` are deliberately thin: the wrapper carries the marketplace metadata and a `.mcp.json` when relevant; the actual skill content is installed from the upstream repo via the `npx … init` command documented in each wrapper's README.

## How `marketplace.json` is generated

The Claude Code marketplace schema has no `import`/`include` for chaining upstream marketplaces — every plugin must be its own `source` block. So the file is generated:

- [`scripts/marketplace-sources.json`](scripts/marketplace-sources.json) is the source of truth (local plugins + upstream marketplace pointers + per-upstream `include` filters and category overrides).
- [`scripts/build-marketplace.py`](scripts/build-marketplace.py) fetches each upstream's `.claude-plugin/marketplace.json` at the pinned SHA and inlines every plugin entry as a `git-subdir` or `url` source, so drill-down install works directly from this marketplace.

Regenerate locally:

```bash
python3 scripts/build-marketplace.py
claude plugin validate .
```

CI rejects PRs where the committed `marketplace.json` doesn't match what the script produces (see [`build-check.yml`](.github/workflows/build-check.yml)).

## Authoring a new plugin

1. Copy the template and rename it:

   ```bash
   cp -R plugins/example-plugin plugins/your-plugin
   $EDITOR plugins/your-plugin/.claude-plugin/plugin.json
   ```

   The template demonstrates every supported asset type (skills, slash commands, agents, MCP servers) — keep what you need, delete the rest.

2. Add an entry to [`scripts/marketplace-sources.json`](scripts/marketplace-sources.json):
   - **Local plugins** (authored in this repo) → push into `local_plugins`.
   - **Mirroring another marketplace** → push into `upstream_marketplaces` with a pinned SHA, optional `include` filter, and optional `category_overrides`.

3. Regenerate and validate:

   ```bash
   python3 scripts/build-marketplace.py
   claude plugin validate .
   ```

4. Open a PR. CI runs all four workflows automatically.

## Automation

Four workflows live in [`.github/workflows`](.github/workflows). All adapted from [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), scoped down to what a personal marketplace needs.

| Workflow | Fires on | What it does |
| --- | --- | --- |
| `validate-plugins.yml` | PR + push to `main` (paths-filtered) | Runs Anthropic's reusable `validate-plugins` action (SHA-pinned). Catches marketplace-schema breaks. |
| `build-check.yml` | PR + push to `main` | Regenerates `marketplace.json` and fails if the committed file drifts. Forces edits to go through the sources file. |
| `validate-frontmatter.yml` | PR + push to `main` | Lints YAML frontmatter on every `skills/*/SKILL.md`, `agents/*.md`, `commands/*.md`. |
| `bump-upstreams.yml` | Cron `0 6 * * *` UTC + manual dispatch | Polls every upstream pin via the GitHub API. Moved SHAs are bumped, `marketplace.json` is regenerated and validated inline, then a PR is opened and squash-merged automatically. |

### Repo settings required by `bump-upstreams.yml`

For the nightly bump PR to open and merge itself, GitHub needs two switches:

1. **Settings → Actions → General → Workflow permissions** — set **Read and write permissions** and tick **Allow GitHub Actions to create and approve pull requests**.
2. **Settings → General → Pull Requests** — keep **Allow squash merging** enabled (default).

Without (1), `gh pr create` from the workflow returns 403. Without (2), the `--squash` merge call fails.

### Manually trigger the bump sweep

```text
Actions → Bump Upstream SHAs → Run workflow → main
```

If all upstreams are at HEAD already, the run exits with `No upstream SHAs moved.`

## Contributing

Open a PR with:

1. New plugin assets (under `plugins/` or `external_plugins/`) with `.claude-plugin/plugin.json` + `README.md`.
2. An entry in `scripts/marketplace-sources.json`.
3. A regenerated `.claude-plugin/marketplace.json` (run `python3 scripts/build-marketplace.py` before pushing).

CI must be green before merge — `validate-plugins`, `build-check`, and `validate-frontmatter` all run on every PR.

## License

Each plugin links to its upstream license. The marketplace metadata in this repo is MIT-licensed unless a plugin folder states otherwise.
