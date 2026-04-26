#!/usr/bin/env bash
set -euo pipefail
command -v uv >/dev/null && uv sync 2>/dev/null || true
mkdir -p .forge/journey
echo "[prewarm] cgse-mod-1 ready"
