#!/usr/bin/env python3
"""Bump pinned upstream SHAs in scripts/marketplace-sources.json.

For each external pin in the sources file, query the GitHub API for the
current HEAD sha of the ref (default `main`). If it has moved, update the
sources file in place. The companion workflow then regenerates
marketplace.json from the updated sources, validates, and opens a PR.

Scope: bumps two places —

1. Every entry in `upstream_marketplaces[*]` (`url`, `ref`, `sha`).
2. Every `local_plugins[*].upstream` block that carries `url` + `sha` —
   wrapper plugins where we vendor metadata locally but want to track
   the upstream tag for `homepage` and refresh prompts.

Auth: uses GITHUB_TOKEN from env (set by the workflow). Anonymous calls
work but burn the unauthenticated rate limit fast.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_PATH = REPO_ROOT / "scripts" / "marketplace-sources.json"
GH_REPO_RE = re.compile(r"^https://github\.com/([^/]+)/([^/.]+?)(?:\.git)?/?$")


def gh_head_sha(repo_url: str, ref: str) -> str | None:
    """Return the current HEAD sha for <repo>@<ref>, or None on 404."""
    match = GH_REPO_RE.match(repo_url)
    if not match:
        print(f"  skip: not a github.com URL: {repo_url}", file=sys.stderr)
        return None
    owner, repo = match.group(1), match.group(2)
    api = f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
    req = urllib.request.Request(api, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["sha"]
    except urllib.error.HTTPError as exc:
        print(f"  ! HTTP {exc.code} fetching {api}", file=sys.stderr)
        return None


def bump_in_place(cfg: dict[str, Any]) -> int:
    """Walk the config, bump every stale sha, return the count of changes."""
    changes = 0

    for entry in cfg.get("upstream_marketplaces", []):
        url = entry["url"]
        ref = entry.get("ref", "main")
        old = entry["sha"]
        print(f"upstream marketplace: {url}@{ref}")
        new = gh_head_sha(url, ref)
        if new and new != old:
            entry["sha"] = new
            print(f"  bumped: {old[:12]} → {new[:12]}")
            changes += 1
        elif new:
            print(f"  unchanged ({old[:12]})")

    for plugin in cfg.get("local_plugins", []):
        upstream = plugin.get("upstream")
        if not upstream or "url" not in upstream or "sha" not in upstream:
            continue
        url = upstream["url"]
        if not url.endswith(".git"):
            url_git = f"{url}.git"
        else:
            url_git = url
        ref = upstream.get("ref", "main")
        old = upstream["sha"]
        print(f"local plugin {plugin['name']}: {url}@{ref}")
        new = gh_head_sha(url_git, ref)
        if new and new != old:
            upstream["sha"] = new
            print(f"  bumped: {old[:12]} → {new[:12]}")
            changes += 1
        elif new:
            print(f"  unchanged ({old[:12]})")

    return changes


def main() -> int:
    with SOURCES_PATH.open() as fh:
        cfg = json.load(fh)

    changes = bump_in_place(cfg)

    if changes == 0:
        print("\nNo upstream SHAs moved.")
        return 0

    with SOURCES_PATH.open("w") as fh:
        json.dump(cfg, fh, indent=2)
        fh.write("\n")

    print(f"\nBumped {changes} pinned sha(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
