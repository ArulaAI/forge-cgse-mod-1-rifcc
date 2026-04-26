#!/usr/bin/env bash
# F4 /hypothesis — Claude Code adapter invoke script.
# Usage:
#   invoke.sh --scaffold <target_dir> [--backend bedrock|mock]
#   invoke.sh --validate <hypothesis_file> --evidence <text> [--backend bedrock|mock]
# Exit codes: 0 = success, 1 = error, 2 = missing shared module
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRIMITIVE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [ ! -f "${PRIMITIVE_ROOT}/shared/scaffolder.py" ]; then
  echo "ERROR: cannot locate scaffolder.py at ${PRIMITIVE_ROOT}/shared/" >&2
  exit 2
fi

PYTHON_BIN="${PYTHON:-python3}"
exec "${PYTHON_BIN}" -m primitives.hypothesis.shared "$@"
