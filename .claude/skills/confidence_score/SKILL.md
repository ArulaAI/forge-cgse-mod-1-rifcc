---
name: confidence-score
description: Rate any artifact Low/Medium/High confidence; gate blocks implementation until >= Medium. Invoke before writing code, before committing a spec, or inside a PreToolUse hook on Write/Edit events.
---

# /confidence-score

Claude Code adapter for the Forge primitive library F1 primitive.

## When invoked

1. Determine the target artifact — user-mentioned path, else `.`
2. Determine the threshold — user-supplied `--threshold Low|Medium|High`, else `Medium`
3. Determine the output format — user-supplied `--format text|json`, else `text`
4. Run: `bash <skill_dir>/invoke.sh <target> [--threshold <level>] [--format <fmt>] [--context <text>]`
5. Parse output. On non-zero exit (gate blocked or error), surface the score level, per-dimension reasoning, and a recommendation to address the lowest-scoring dimensions before proceeding.

## Output expectations

- Always surface the final score level (Low / Medium / High)
- For each dimension, show the dimension name, score, and one-sentence reasoning
- If the gate blocks (exit code 1), state clearly which threshold was required and what was scored, and recommend the learner improve the lowest-scoring dimensions before continuing
- If the gate passes (exit code 0), confirm success and encourage proceeding

## Invariants

- Logic lives in `primitives/confidence_score/shared/scorer.py` in the Forge primitive library
- DO NOT modify `invoke.sh` or duplicate scorer logic — primitive library upgrades flow through `forge sync`

## PreToolUse hook example

To gate every Write/Edit event automatically, add this to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .forge/primitives/confidence_score/adapters/claude_code/invoke.sh $CLAUDE_TOOL_INPUT_FILE_PATH --threshold Medium"
          }
        ]
      }
    ]
  }
}
```
