---
name: autowork
description: Autonomous development loop — works through issues, routes to domains, implements against acceptance criteria, validates, creates PRs, reviews, and merges. Use /autowork --dry-run to preview; /autowork to execute.
---

# /autowork

Claude Code adapter for the Forge primitive library U5 primitive.

## When invoked

1. Determine the lab/repo root — current directory by default
2. Determine flags — `--dry-run`, `--label <label>`, `--max-issues <n>`, `--source <github|markdown>`, `--resume`
3. Run: `bash <skill_dir>/invoke.sh <lab_root> [flags]`
4. In dry-run mode: display the planned execution order
5. In full mode: the orchestrator manages the loop; this adapter provides the harness agent surface for implementation steps

## Output expectations

- Dry run: ordered list of issues with domain, stack, complexity, and criteria count
- Full run: per-issue progress (branch, criteria, PR, review, merge), then session summary

## Invariants

- Logic lives in `primitives/autowork/shared/` in the Forge primitive library
- DO NOT duplicate orchestrator logic — primitive library upgrades flow through `forge sync`
- Configuration lives in `.forge/autowork.yaml` (per-repo)
