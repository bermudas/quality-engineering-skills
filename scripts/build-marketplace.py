#!/usr/bin/env python3
"""Generate .claude-plugin/marketplace.json from scripts/marketplace-sources.json.

The Claude Code marketplace schema has no `import`/`include` for chaining
upstream marketplaces, so this script does it at build time:

- `local_plugins` entries are emitted verbatim (they reference paths inside
  this repo, like `./external_plugins/elitea-next`).
- For each `upstream_marketplaces` entry, the script fetches the upstream's
  `.claude-plugin/marketplace.json` at the pinned sha and converts every
  plugin entry into either a `git-subdir` or `url` source pointing at the
  same sha. `include` filters by name (`["*"]` keeps all);
  `category_overrides` lets you re-bucket individual plugins.

Run:

    python3 scripts/build-marketplace.py

The script is dependency-free (stdlib only) so it works without setting up
a venv.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_PATH = REPO_ROOT / "scripts" / "marketplace-sources.json"
OUTPUT_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def fetch_upstream_marketplace(repo_url: str, sha: str) -> dict[str, Any]:
    """Fetch <repo>/.claude-plugin/marketplace.json at the given commit sha."""
    if not repo_url.endswith(".git"):
        raise ValueError(f"upstream url must end with .git: {repo_url}")
    raw = repo_url[: -len(".git")].replace("github.com", "raw.githubusercontent.com")
    url = f"{raw}/{sha}/.claude-plugin/marketplace.json"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"failed to fetch {url}: HTTP {exc.code}") from exc


def relative_subpath(source: str) -> str:
    """Normalize an upstream `source` like './agents/ba' or './' into a clean
    subpath ('agents/ba' or ''). Refuses absolute paths and parent-traversal."""
    s = source.strip()
    if s.startswith("./"):
        s = s[2:]
    if s in ("", "/", "."):
        return ""
    if s.startswith("/") or ".." in Path(s).parts:
        raise ValueError(f"refusing unsafe upstream source path: {source!r}")
    return s.rstrip("/")


def kind_prefix_for(subpath: str) -> str:
    """Tag mirrored upstream entries so the `/plugin` picker shows at a glance
    whether a row is the umbrella bundle or a single drilled-down component.

    Heuristic from the upstream source path:
      ""           -> [Bundle]  (root install — usually carries .mcp.json + all components)
      agents/...   -> [Agent]
      skills/...   -> [Skill]
      anything else -> no prefix
    """
    if subpath == "":
        return "[Bundle] "
    first = subpath.split("/", 1)[0]
    if first == "agents":
        return "[Agent] "
    if first == "skills":
        return "[Skill] "
    return ""


def emit_from_upstream(
    plugin: dict[str, Any],
    upstream_repo_url: str,
    upstream_ref: str,
    upstream_sha: str,
    default_category: str,
    category_overrides: dict[str, str],
    author_override: dict[str, str] | None,
) -> dict[str, Any]:
    """Convert one upstream plugin entry into our marketplace.json shape."""
    subpath = relative_subpath(plugin["source"])
    homepage_base = upstream_repo_url.removesuffix(".git")

    if subpath == "":
        source_block = {
            "source": "url",
            "url": upstream_repo_url,
            "ref": upstream_ref,
            "sha": upstream_sha,
        }
        homepage = homepage_base
    else:
        source_block = {
            "source": "git-subdir",
            "url": upstream_repo_url,
            "path": subpath,
            "ref": upstream_ref,
            "sha": upstream_sha,
        }
        homepage = f"{homepage_base}/tree/{upstream_ref}/{subpath}"

    entry: dict[str, Any] = {
        "name": plugin["name"],
        "description": kind_prefix_for(subpath) + plugin.get("description", ""),
    }
    if author_override:
        entry["author"] = author_override
    elif "author" in plugin:
        entry["author"] = plugin["author"]

    entry["category"] = category_overrides.get(plugin["name"], default_category)
    entry["source"] = source_block
    entry["homepage"] = homepage
    return entry


def strip_nonstandard_fields(plugin: dict[str, Any]) -> dict[str, Any]:
    """Drop fields Claude Code's marketplace loader doesn't recognize.

    `upstream` is useful documentation in our sources file but the marketplace
    schema only allows the documented plugin manifest fields plus `source`,
    `category`, `tags`, `strict`. Anything else triggers a validator warning.
    """
    return {k: v for k, v in plugin.items() if k != "upstream"}


def build() -> dict[str, Any]:
    with SOURCES_PATH.open() as fh:
        cfg = json.load(fh)

    plugins: list[dict[str, Any]] = []
    plugins.extend(strip_nonstandard_fields(p) for p in cfg.get("local_plugins", []))

    for upstream in cfg.get("upstream_marketplaces", []):
        repo_url = upstream["url"]
        ref = upstream.get("ref", "main")
        sha = upstream["sha"]
        include = set(upstream.get("include", ["*"]))
        category_overrides = upstream.get("category_overrides", {})
        default_category = upstream.get("default_category", "development")
        author_override = upstream.get("author")

        upstream_market = fetch_upstream_marketplace(repo_url, sha)
        upstream_plugins = upstream_market.get("plugins", [])
        for plugin in upstream_plugins:
            if "*" not in include and plugin["name"] not in include:
                continue
            entry = emit_from_upstream(
                plugin,
                upstream_repo_url=repo_url,
                upstream_ref=ref,
                upstream_sha=sha,
                default_category=default_category,
                category_overrides=category_overrides,
                author_override=author_override,
            )
            plugins.append(entry)

    output = dict(cfg["marketplace"])
    output["plugins"] = plugins
    return output


def main() -> int:
    output = build()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w") as fh:
        json.dump(output, fh, indent=2)
        fh.write("\n")

    names = [p["name"] for p in output["plugins"]]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        print(f"ERROR: duplicate plugin names: {sorted(dupes)}", file=sys.stderr)
        return 1
    print(f"Wrote {OUTPUT_PATH} with {len(output['plugins'])} plugins.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
