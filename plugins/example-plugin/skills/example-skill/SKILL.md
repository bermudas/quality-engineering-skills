---
name: example-skill
description: Replace this description with the trigger conditions for your skill. Be specific — list the phrases, file shapes, or task contexts that should activate it. Example, "Use whenever the user asks to bootstrap a new qavajs project, or when a `qavajs.config.{js,ts}` file is in scope, or when they say 'add a step definition'."
---

# Example Skill

This is a placeholder for a **model-invoked skill**. The agent reads `description` (above) to decide when to activate this skill, then reads this body for the actual guidance.

## What to put here

- **Why this skill exists** — the problem it solves and the discipline it enforces.
- **Workflow / phases** — numbered, in order. Skills work best when they keep the agent on rails.
- **Footguns** — surprising behaviors, validation gates, ordering constraints.
- **References** — link to files in this skill's folder (e.g. `references/example.md`) the agent should read before acting.

Keep it terse. The agent re-reads the whole file when the skill activates — long preambles burn tokens.
