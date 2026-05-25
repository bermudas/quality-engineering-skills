# example-plugin

Reference template for plugins authored directly in this marketplace. Copy this directory, rename it (kebab-case), and edit the assets you need.

## Layout

```
example-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required — name, description, author, homepage
├── .mcp.json                # Optional — MCP servers this plugin provides
├── commands/                # Optional — legacy slash-command markdown files
│   └── example-command.md
├── agents/                  # Optional — agent definitions
│   └── example-agent.md
├── skills/                  # Preferred for both model- and user-invoked capabilities
│   └── example-skill/
│       └── SKILL.md
└── README.md
```

You only need `.claude-plugin/plugin.json`. Everything else is optional — keep what you use, delete the rest.

## Asset types

- **Skills** (`skills/<name>/SKILL.md`) — preferred for both model-invoked guidance and user-invoked slash commands. The front-matter `name`, `description`, and (for slash commands) `argument-hint` / `allowed-tools` control how it's triggered.
- **Commands** (`commands/<name>.md`) — legacy slash-command layout. Loaded identically to `skills/<name>/SKILL.md`. Prefer `skills/` for new work.
- **Agents** (`agents/<name>.md`) — sub-agent definitions with their own system prompt and tool allowlist.
- **MCP servers** (`.mcp.json`) — top-level keys are server names. Supports `stdio`, `http`, `sse`. Reference env vars with `${VAR}` so configuration can stay in the user's `.env`.

## Publish

1. Pick a name (kebab-case) and rename this directory.
2. Update `.claude-plugin/plugin.json`.
3. Add an entry to `/.claude-plugin/marketplace.json` with `"source": "./plugins/<your-name>"`.
4. Test locally: `/plugin marketplace add <local-path>` then `/plugin install <your-name>@quality-engineering-skills`.

For more, see the [official plugin docs](https://code.claude.com/docs/en/plugins).
