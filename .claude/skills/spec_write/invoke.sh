#!/usr/bin/env bash
# F5 /spec-write — Claude Code adapter invoke script.
# Usage: invoke.sh [target_dir] [--output PATH] [--dry-run] [--backend mock|bedrock] [--context TEXT]
# Exit codes: 0 = spec written (or dry-run); 1 = self-review found blocking issues; 2 = fatal error
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRIMITIVE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [ ! -f "${PRIMITIVE_ROOT}/shared/__init__.py" ]; then
  echo "ERROR: cannot locate shared package at ${PRIMITIVE_ROOT}/shared/" >&2
  exit 2
fi

PYTHON_BIN="${PYTHON:-python3}"
exec "${PYTHON_BIN}" -m primitives.spec_write.shared "$@"
