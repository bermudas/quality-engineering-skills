# qaspace-skill

Wrapper for [bermudas/qaspace-skill](https://github.com/bermudas/qaspace-skill) — an [agentskills.io](https://agentskills.io) skill for querying the **EPAM qaspace Test Management Plugin** on Jira Server / Data Center.

> Naming note: this targets EPAM's *qaspace* (the Jira `TM` plugin), **not** Tricentis qTest, despite the common "qtest" misnomer. The skill keeps "qtest" as a trigger alias.

## What the skill teaches your agent

- Discover custom-field IDs (`GET /rest/api/2/field`) and cache them per project — the numeric `customfield_*` ids vary by install order, the field *names* don't.
- Resolve test runs by name or id, then narrow by folder, status, type via JQL.
- Build the folder tree the fast way (single `/rest/tm/1.0/folder/list` call) with a JQL-sweep fallback for hardened installs.
- Triage for automation — runnable manuals, automated-but-pending, failed-only, exclude out-of-scope.
- Paginate large runs economically (two-field folder sweeps, cost tables, smallest `fields` set per use case).
- Avoid plugin footguns — `cf[24001]` only supports `=`, the `search_using_jql` MCP tool's 5-result cap, the doubly-encoded MCP folder-list response, TM-Status vs Jira workflow-status confusion.

## Install

1. From this marketplace:

   ```bash
   /plugin install qaspace-skill@quality-engineering-skills
   ```

2. Then install the actual skill files into your project (follow upstream README — agentskills.io install pattern):

   ```bash
   cd your-project
   # see https://github.com/bermudas/qaspace-skill#install for the current command
   ```

## Upstream

- Repo: <https://github.com/bermudas/qaspace-skill>
- Skill spec: [`skill-spec.md`](https://github.com/bermudas/qaspace-skill/blob/main/skill-spec.md)
- Pinned: see `sha` in the marketplace.json entry
