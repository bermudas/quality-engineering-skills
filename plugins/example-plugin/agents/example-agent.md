---
name: example-agent
description: When to spawn this sub-agent. Be specific about the task shape — what inputs it expects and what kind of output it returns.
tools: [Read, Glob, Grep, Bash]
---

# example-agent

Placeholder for a **sub-agent definition**. The main agent spawns this one via the Agent tool when the user's task matches `description`.

## What to put here

- **The sub-agent's role and scope** — what it owns, what it doesn't.
- **System prompt** — the persona, conventions, output format the sub-agent should follow.
- **Tool budget** — which tools it may use (already declared in `tools:` above).
- **Stopping conditions** — when to return control to the main agent vs. keep going.

Sub-agents are best for tasks that are independent of the main conversation context (research, lookups, parallel work) or that benefit from a focused tool allowlist.
