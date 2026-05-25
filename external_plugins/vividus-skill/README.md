# vividus-skill

Wrapper for [bermudas/vividus-skill](https://github.com/bermudas/vividus-skill) — an [agentskills.io](https://agentskills.io) skill for the **Vividus** test automation framework.

## What the skill teaches your agent

- **Bootstrap** a new Vividus project (Gradle/Maven layout, properties, suites).
- **Configure** environments, profiles, and runtime properties without breaking the precedence rules.
- **Author** scenarios using Vividus's BDD DSL — steps, examples, lifecycle hooks.
- **Run** suites locally and in CI, including Allure + Vividus reporting.

## Install

1. Marketplace entry:

   ```bash
   /plugin install vividus-skill@quality-engineering-skills
   ```

2. Install the skill files into your project (follow upstream commands):

   ```bash
   cd your-project
   # see https://github.com/bermudas/vividus-skill#install
   ```

## Upstream

- Repo: <https://github.com/bermudas/vividus-skill>
- Skill spec: [`skill-spec.md`](https://github.com/bermudas/vividus-skill/blob/main/skill-spec.md)
- Vividus project: <https://github.com/vividus-framework/vividus>
- Pinned: see `sha` in the marketplace.json entry
