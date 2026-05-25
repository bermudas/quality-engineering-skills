---
name: example-command
description: Short description shown in /help. Use when the user types /example-command.
argument-hint: <required-arg> [optional-arg]
allowed-tools: [Read, Glob, Grep, Bash]
---

# /example-command

Placeholder for a **user-invoked slash command**.

When the user types `/example-command <args>`, Claude reads this file and follows the instructions below.

## What to put here

- **What the command does** in one sentence.
- **Steps to perform** when invoked — concrete, numbered.
- **Arguments** — describe each one declared in `argument-hint` and how to parse `$ARGUMENTS`.
- **Output format** — what the user should see.

The legacy `commands/<name>.md` layout is equivalent to `skills/<name>/SKILL.md`. Prefer the `skills/` directory for new work.
