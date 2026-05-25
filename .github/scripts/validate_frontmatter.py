#!/usr/bin/env python3
"""Validate YAML frontmatter on every skill/agent/command markdown file.

Walks the repo, parses the `---`-delimited frontmatter block at the top of
each file, and checks the documented required fields per file type:

- `skills/<name>/SKILL.md`: `name`, `description`
- `commands/<name>.md`:     `name`, `description`
- `agents/<name>.md`:       `name`, `description`

Extra fields are allowed. Missing required fields, malformed YAML, or
missing frontmatter blocks fail the run with a clear message.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def iter_targets() -> Iterable[tuple[Path, str]]:
    for p in REPO_ROOT.rglob("skills/*/SKILL.md"):
        yield p, "skill"
    for p in REPO_ROOT.rglob("agents/*.md"):
        yield p, "agent"
    for p in REPO_ROOT.rglob("commands/*.md"):
        yield p, "command"


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    rest = text[3:].lstrip("\n")
    end = rest.find("\n---")
    if end < 0:
        return None
    block = rest[:end]
    parsed = yaml.safe_load(block)
    if not isinstance(parsed, dict):
        return None
    return parsed


def validate(path: Path, kind: str) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(REPO_ROOT)
    try:
        fm = parse_frontmatter(path)
    except yaml.YAMLError as exc:
        return [f"{rel}: invalid YAML frontmatter — {exc}"]

    if fm is None:
        return [f"{rel}: missing or unterminated YAML frontmatter block"]

    for field in ("name", "description"):
        if not fm.get(field):
            errors.append(f"{rel}: missing required field '{field}' in frontmatter")

    return errors


def main() -> int:
    all_errors: list[str] = []
    count = 0
    for path, kind in iter_targets():
        count += 1
        all_errors.extend(validate(path, kind))

    if all_errors:
        for err in all_errors:
            print(f"::error::{err}")
        print(f"\n{len(all_errors)} frontmatter issue(s) in {count} file(s).", file=sys.stderr)
        return 1

    print(f"Validated {count} markdown frontmatter blocks. All good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
