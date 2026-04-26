#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
WALKER="$REPO_ROOT/.forge/local/primitives/walk-rifcc/shared/walker.py"
[[ -f "$WALKER" ]] || { echo "walker.py not found" >&2; exit 2; }
cd "$REPO_ROOT"
if command -v uv >/dev/null 2>&1; then exec uv run python "$WALKER" "$@"
else exec python3 "$WALKER" "$@"; fi
