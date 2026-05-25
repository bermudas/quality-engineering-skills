# qa-agent

Wrapper for [onetest-ai/qa-agent](https://github.com/onetest-ai/qa-agent) — a composable QA agent that installs multi-specialist analysis, exploratory testing, accessibility, security, and test generation into any project. Works with Claude Code, Cursor, Windsurf, GitHub Copilot, and Octobots.

## Why a wrapper

The upstream is distributed as an `npx` installer that writes agent + skill files into your project. It's not a Claude Code plugin in the strict sense, so this wrapper exists to surface it in this marketplace and document the install flow.

## Install

1. Install the marketplace entry (registers this plugin in `/plugin`):

   ```bash
   /plugin install qa-agent@quality-engineering-skills
   ```

2. Inside your project, run the upstream interactive installer:

   ```bash
   cd your-project
   npx github:onetest-ai/qa-agent init
   ```

   This walks you through prerequisites, target tools, skill selection, MCP servers, and credential setup. Non-interactive variants:

   ```bash
   npx github:onetest-ai/qa-agent init --all      # all skills, no MCP, Claude Code target
   npx github:onetest-ai/qa-agent init --update   # refresh agents + skills, preserve settings
   ```

## Use

After install, start the QA agent and onboard it to your product:

```bash
claude --agent qa
> /qa-init
```

`/qa-init` is a 6-phase pipeline: interview → pre-flight → ingest → synthesize → configure → verify. See the upstream README for the full flow.

## Upstream

- Repo: <https://github.com/onetest-ai/qa-agent>
- License: Apache-2.0
- Pinned: see `sha` in the marketplace.json entry
