#!/usr/bin/env bash
# Refresh the vendored agent-evaluator skill from dshaplyko/skills.
# Usage: SHA=<commit-sha> ./scripts/vendor-from-upstream.sh
# If SHA is unset, latest main is used and printed at the end so you can pin it.
set -euo pipefail

SHA="${SHA:-main}"
BASE="https://raw.githubusercontent.com/dshaplyko/skills/${SHA}/.claude/skills/agent-evaluator"
DEST="$(cd "$(dirname "$0")/.." && pwd)/skills/agent-evaluator"

mkdir -p "${DEST}/references"
curl -fsSL "${BASE}/SKILL.md" -o "${DEST}/SKILL.md"
for f in clarifying_questions.md example_report.html maturity_model_requirements.md report_template.md scoring_rubric.md; do
  curl -fsSL "${BASE}/references/${f}" -o "${DEST}/references/${f}"
done

if [[ "${SHA}" == "main" ]]; then
  RESOLVED="$(curl -fsSL "https://api.github.com/repos/dshaplyko/skills/commits/main" | grep -m1 '"sha":' | sed -E 's/.*"sha": "([^"]+)".*/\1/')"
  echo
  echo "Vendored from latest main. Pin this SHA in marketplace.json:"
  echo "  ${RESOLVED}"
fi
