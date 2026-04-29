---
name: autowork
description: Autonomous development loop — works through open issues, routes to domains, implements, validates, creates PRs, and merges. Requires .forge/autowork.yaml configuration.
tools:
  - shell
---

# Skill: autowork

Autonomous development loop that processes open issues sequentially. Each issue is routed to a domain (from `.forge/autowork.yaml`), implemented criterion by criterion, validated, PR'd, reviewed, and merged.

## How to invoke

Run from repo root:

```bash
python .forge/primitives/autowork/shared/orchestrator.py . --dry-run
```

Or for full execution:

```bash
python .forge/primitives/autowork/shared/orchestrator.py . --source markdown
```

## Configuration

Requires `.forge/autowork.yaml` with at least one domain defined. See SPEC.md for full schema.

## Invariants

- Wraps `.forge/primitives/autowork/shared/orchestrator.py` — DO NOT duplicate logic
- Updates land via `forge sync` per the lab's `.forge/manifest.yaml` pin
