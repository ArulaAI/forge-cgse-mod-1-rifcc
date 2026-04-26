---
name: confidence-score
description: Rate artifact confidence Low/Medium/High against a 5-dimension rubric. Gate blocks implementation when score is below threshold. Available to coding agent + CLI + chat.
tools:
  - shell
---

# Skill: confidence-score

Rate a spec, hypothesis, or code artifact Low / Medium / High confidence against five rubric dimensions (specificity, error handling, testability, dependency clarity, security consideration). Exits non-zero when the artifact scores below the requested threshold.

## How to invoke

Run from repo root:

```bash
python .forge/primitives/confidence_score/shared/scorer.py {input:target|.} --format json
```

Or use the slash command `/confidence-score <target>` from `prompts/confidence-score.prompt.md`.

## Output

JSON object with:
- `level`: `"low"` | `"medium"` | `"high"`
- `weighted_score`: float 0.0–1.0
- `dimensions`: list of `{id, score, reasoning}`
- `gate_passed`: boolean

## When to use

- Before writing implementation code — gate on the feature spec
- Before committing a `hypothesis.md` — confirm the hypothesis is well-formed
- Before merging a feature PR — confirm the implementation spec still holds
- As a `preToolUse` hook on Write/Edit events (see Claude Code adapter for hook snippet)

## Invariants

- Wraps `.forge/primitives/confidence_score/shared/scorer.py` — DO NOT duplicate logic
- Updates land via `forge sync` per the lab's `.forge/manifest.yaml` pin
