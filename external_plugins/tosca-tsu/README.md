# tosca-tsu

Wrapper for [bermudas/ToscaTSU](https://github.com/bermudas/ToscaTSU) — a bidirectional bridge between Tricentis Tosca `.tsu` test bundles and Playwright TypeScript specs.

## What it does

- `parse_tsu.py` — read a `.tsu` and emit Playwright TypeScript specs.
- `gen_tsu.py` — take Playwright specs and emit a `.tsu` bundle Tosca can ingest.
- `spec_to_manifest.py` — turn a Playwright spec into a Tosca-compatible manifest.
- Bundled Playwright MCP for VS Code, Copilot, and Copilot CLI so the agent can drive the browser while translating.

## Install

1. Marketplace entry:

   ```bash
   /plugin install tosca-tsu@quality-engineering-skills
   ```

2. Install the skill bundle and helpers into your project — the upstream ships an installer:

   ```bash
   cd your-project
   curl -fsSL https://raw.githubusercontent.com/bermudas/ToscaTSU/main/install-from-github.sh | bash
   # or clone + run ./install.sh from a local copy
   ```

## Upstream

- Repo: <https://github.com/bermudas/ToscaTSU>
- Tricentis Tosca: <https://www.tricentis.com/products/automate-continuous-testing-tosca>
- Pinned: see `sha` in the marketplace.json entry
