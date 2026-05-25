# Quality Engineering Skills

A Claude Code plugin marketplace focused on **quality engineering, test automation, and SDLC tooling**. Curated and maintained by [@bermudas](https://github.com/bermudas).

> **⚠️ Trust before installing.** Plugins listed here run MCP servers and skills that may have access to your code, secrets, and external systems. Inspect each plugin's source before installing, updating, or using it.

## Structure

- **`/plugins`** — Plugins authored in this repo.
- **`/external_plugins`** — Thin in-repo wrappers around upstream skill bundles and MCP servers (e.g. `npx`-installable skill packs, hosted MCP endpoints). Each wrapper carries a `plugin.json` and points at the canonical upstream repo.
- **`/.claude-plugin/marketplace.json`** — The marketplace manifest indexing every plugin in this repo and any pinned third-party plugins (e.g. `sdlc-skills`).

## Install this marketplace

```bash
# Inside Claude Code:
/plugin marketplace add bermudas/quality-engineering-skills
/plugin install <plugin-name>@quality-engineering-skills
```

Or browse it interactively with `/plugin > Discover` after adding the marketplace.

## Plugins

| Plugin | Source | What it does |
| --- | --- | --- |
| [`elitea-next`](external_plugins/elitea-next) | in-repo (SSE MCP) | Connect Claude Code to an EPAM **ELITEA Next** project over SSE. Reads project id + token from a local `.env`. |
| [`qa-agent`](external_plugins/qa-agent) | wraps [onetest-ai/qa-agent](https://github.com/onetest-ai/qa-agent) | Multi-specialist QA agent — exploratory testing, accessibility, security, test generation, with onboarding pipeline. |
| [`sdlc-skills`](https://github.com/arozumenko/sdlc-skills) | external (proper plugin marketplace) | BA, Tech Lead, PM, Python/JS/iOS dev, QA agents plus skills for bug-fix, feature planning, code review, TDD. |
| [`servicenow-atf-skill`](https://github.com/bermudas/servicenow-atf-skill) | external (proper plugin marketplace) | ServiceNow ATF — Fluent SDK (`now-sdk build/install`) and a zero-install Scripted-REST builder for `glide_var` step inputs. |
| [`agent-evaluator`](external_plugins/agent-evaluator) | vendors [dshaplyko/skills/.../agent-evaluator](https://github.com/dshaplyko/skills/tree/main/.claude/skills/agent-evaluator) | Score AI agent specifications against the Agent Maturity Model (L0–L3, 39 practices) and emit a styled HTML report. |
| [`qaspace-skill`](external_plugins/qaspace-skill) | wraps [bermudas/qaspace-skill](https://github.com/bermudas/qaspace-skill) | Query EPAM **qaspace** Test Management Plugin on Jira Server/DC via JQL or MCP. |
| [`qavajs-skill`](external_plugins/qavajs-skill) | wraps [bermudas/qavajs-skill](https://github.com/bermudas/qavajs-skill) | qavajs BDD framework — 270 step patterns, full config and DSL reference. |
| [`vividus-skill`](external_plugins/vividus-skill) | wraps [bermudas/vividus-skill](https://github.com/bermudas/vividus-skill) | Vividus test automation framework — bootstrap, configure, author, run. |
| [`tosca-tsu`](external_plugins/tosca-tsu) | wraps [bermudas/ToscaTSU](https://github.com/bermudas/ToscaTSU) | Bidirectional bridge between Tricentis Tosca `.tsu` bundles and Playwright TypeScript specs. |
| [`toscacloud-cli`](external_plugins/toscacloud-cli) | wraps [bermudas/toscacloud_cli](https://github.com/bermudas/toscacloud_cli) | AI-native CLI for Tricentis Tosca Cloud. |

## Authoring a new plugin

Copy [`plugins/example-plugin`](plugins/example-plugin) and rename it. The template demonstrates every supported asset type (skills, slash commands, agents, MCP servers) so you can keep what you need and delete the rest.

```bash
cp -R plugins/example-plugin plugins/your-plugin
$EDITOR plugins/your-plugin/.claude-plugin/plugin.json
# Then add an entry under "plugins" in .claude-plugin/marketplace.json
```

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

Wrapper plugins under `/external_plugins` are deliberately thin. The wrapper carries the marketplace metadata and a `.mcp.json` when relevant; the actual skill content is installed from the upstream repo via the `npx … init` command documented in each wrapper's README.

## Contributing

Want to add a plugin? Open a PR that:

1. Adds a directory under `/plugins` (authored here) or `/external_plugins` (wrapper around an upstream repo).
2. Includes a `.claude-plugin/plugin.json` and a `README.md`.
3. Adds an entry to `.claude-plugin/marketplace.json` — pin external `source: "url"` and `source: "git-subdir"` entries to a specific `sha` so installs are reproducible.

## License

Each plugin links to its upstream license. The marketplace metadata in this repo is MIT-licensed unless a plugin folder states otherwise.
