#!/usr/bin/env bash
# F1 /confidence-score — Claude Code adapter invoke script.
# Usage: invoke.sh <target> [--threshold Low|Medium|High] [--format text|json] [--context <text>]
# Exit codes: 0 = gate passed (score >= threshold), 1 = gate blocked or error, 2 = missing scorer
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRIMITIVE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [ -f "${PRIMITIVE_ROOT}/shared/scorer.py" ]; then
  SCORER="${PRIMITIVE_ROOT}/shared/scorer.py"
else
  echo "ERROR: cannot locate scorer.py at ${PRIMITIVE_ROOT}/shared/" >&2
  exit 2
fi

PYTHON_BIN="${PYTHON:-python3}"
exec "${PYTHON_BIN}" -m primitives.confidence_score.shared.scorer "$@"
