# agent-evaluator

Wrapper for the `agent-evaluator` skill from [dshaplyko/skills](https://github.com/dshaplyko/skills/tree/main/.claude/skills/agent-evaluator). The actual skill files (SKILL.md plus references) are vendored under [`skills/agent-evaluator/`](skills/agent-evaluator) so the plugin install just works.

## What it does

Scores an AI agent specification against the **Agent Maturity Model** (Ihar Bylitski, Feb 2026):

- Four cumulative levels — **L0** Beginner, **L1** Foundational, **L2** Advanced, **L3** Autonomous.
- 39 practices across 9 categories.
- Output is a styled HTML maturity assessment report using the project's house template.

The skill enforces three discipline points missing from ad-hoc reviews:

1. **Consistent scale** — every agent lands on the same L0–L3 anchors, so reports are comparable across clients.
2. **Evidence per claim** — every strength and gap must point to a specific instruction in the agent's spec. No aspirational scoring.
3. **Honest N/A handling** — platform-side practices (token cost, telemetry, eval harness) live outside the agent prompt. The skill asks the user about those before scoring so they aren't mis-marked as gaps.

## Trigger phrases

- "evaluate this agent"
- "score these agents"
- "how mature is X"
- "audit the agent suite in folder Y"
- "rate this prompt against best practices"
- "is this L1 or L2"
- Pointing at a folder of `*_agent.md` / `*.yml` files and asking for an assessment.

## Install

```bash
/plugin install agent-evaluator@quality-engineering-skills
```

That's it — the skill files come with the plugin.

## Refreshing from upstream

This wrapper pins a specific commit of `dshaplyko/skills`. To refresh, bump the `sha` in `.claude-plugin/marketplace.json` and re-run the vendoring command in `scripts/vendor-agent-evaluator.sh` (or pull the latest files manually from the upstream path).

## Upstream

- Path: <https://github.com/dshaplyko/skills/tree/main/.claude/skills/agent-evaluator>
- Pinned SHA: see the marketplace.json entry
