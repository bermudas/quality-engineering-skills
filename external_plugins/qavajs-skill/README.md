# qavajs-skill

Wrapper for [bermudas/qavajs-skill](https://github.com/bermudas/qavajs-skill) — an agent skill for the **qavajs** BDD test automation framework.

## What the skill includes

- **270 step patterns** indexed and searchable so the agent can pick the right step instead of inventing one.
- **Configuration reference** for `qavajs.config.{js,ts}` — profiles, hooks, plugins, parallel mode.
- **DSL reference** — full Gherkin + qavajs extensions, with examples for parameter types and data tables.
- **Playwright MCP** bundled so the agent can drive the browser while authoring or debugging features.

## Install

1. Marketplace entry:

   ```bash
   /plugin install qavajs-skill@quality-engineering-skills
   ```

2. Install the skill files into your project (follow upstream install commands):

   ```bash
   cd your-project
   # see https://github.com/bermudas/qavajs-skill#install
   ```

## Upstream

- Repo: <https://github.com/bermudas/qavajs-skill>
- qavajs project: <https://qavajs.github.io>
- Pinned: see `sha` in the marketplace.json entry
