#!/usr/bin/env bash
# U5 /autowork — Claude Code adapter invoke script.
# Usage: invoke.sh [lab_root] [--dry-run] [--label <label>] [--max-issues <n>] [--source <type>] [--resume]
# Exit codes: 0 = completed, 1 = config error or execution failure
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRIMITIVE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [ -f "${PRIMITIVE_ROOT}/shared/orchestrator.py" ]; then
  ORCHESTRATOR="${PRIMITIVE_ROOT}/shared/orchestrator.py"
else
  echo "ERROR: cannot locate orchestrator.py at ${PRIMITIVE_ROOT}/shared/" >&2
  exit 2
fi

PYTHON_BIN="${PYTHON:-python3}"
exec "${PYTHON_BIN}" -m primitives.autowork.shared.orchestrator "$@"
