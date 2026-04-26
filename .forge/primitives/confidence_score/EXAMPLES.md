# F1 `/confidence-score` — Usage Examples

Five real-world patterns for invoking the confidence scorer in development,
lab exercises, and CI contexts. All examples assume the Forge primitive library
is on `PYTHONPATH` (or installed via `uv`).

---

## 1. Pre-implementation gate on a spec

Rate a spec before writing any code. If the spec scores below Medium the
command exits 1 and blocks the next step.

```bash
# From the lab root — gate spec.md at the default Medium threshold
python -m primitives.confidence_score.shared.scorer exercises/lab-1/spec.md \
  --threshold medium
```

Sample output when the gate passes:

```
Confidence level : HIGH
Weighted score   : 0.7820
Gate passed      : True

  [specificity] 0.90 — States scope and non-goals clearly.
  [error_handling] 0.75 — All three failure modes named.
  [testability] 0.85 — Each criterion is falsifiable.
  [dependency_clarity] 0.72 — Pinned library versions listed.
  [security_consideration] 0.70 — Input sanitisation noted.
```

Sample output when the gate blocks (exits 1):

```
GATE BLOCKED: Confidence gate blocked: level='low' is below threshold='medium' (weighted_score=0.1750)
```

---

## 2. JSON output piped to jq

Use `--format json` to extract machine-readable fields — useful in CI scripts
or when you want to parse only the score level.

```bash
# Print just the confidence level
python -m primitives.confidence_score.shared.scorer src/auth.py \
  --format json | jq '.level'
```

Output:

```json
"medium"
```

Full JSON shape returned by the scorer:

```json
{
  "level": "medium",
  "weighted_score": 0.5620,
  "gate_passed": true,
  "dimensions": [
    { "id": "specificity",          "score": 0.60, "reasoning": "Somewhat specific." },
    { "id": "error_handling",       "score": 0.50, "reasoning": "Some handling." },
    { "id": "testability",          "score": 0.55, "reasoning": "Partial criteria." },
    { "id": "dependency_clarity",   "score": 0.60, "reasoning": "Mostly named." },
    { "id": "security_consideration","score": 0.55, "reasoning": "Brief mention." }
  ]
}
```

Extract the per-dimension table with jq:

```bash
python -m primitives.confidence_score.shared.scorer src/auth.py --format json \
  | jq -r '.dimensions[] | "\(.id)\t\(.score)\t\(.reasoning)"'
```

---

## 3. PreToolUse hook — gate Write/Edit events automatically

Add the following snippet to `.claude/settings.json` (lab root) so that every
time Claude Code is about to write or edit a file, the confidence scorer gates
the action. If the about-to-be-written artifact scores below Medium, the tool
call is blocked and Claude surfaces the per-dimension reasoning.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .forge/primitives/confidence_score/adapters/claude_code/invoke.sh $CLAUDE_TOOL_INPUT_FILE_PATH --threshold medium"
          }
        ]
      }
    ]
  }
}
```

How it works:

1. Claude Code evaluates the PreToolUse hook before executing any `Write` or
   `Edit` tool call.
2. `invoke.sh` resolves `scorer.py` from the `.forge/` tree and invokes it with
   the target path injected via `$CLAUDE_TOOL_INPUT_FILE_PATH`.
3. If the scorer exits 1 (gate blocked), the Write/Edit tool call is cancelled
   and Claude presents the per-dimension reasoning to the learner.
4. The learner revises their spec or code and retries — building the habit of
   confidence-first development.

To require High confidence (stricter, e.g. for final submissions):

```json
"command": "bash .forge/primitives/confidence_score/adapters/claude_code/invoke.sh $CLAUDE_TOOL_INPUT_FILE_PATH --threshold high"
```

---

## 4. Batch check all spec files

Check every `spec.md` across lab exercises in one pass. Exit codes accumulate —
useful as a pre-commit or CI step to surface which exercises have low-quality
specs.

```bash
#!/usr/bin/env bash
# score-all-specs.sh — run from lab root
set -uo pipefail

FAILED=0
for f in exercises/*/spec.md; do
  echo "--- $f ---"
  if ! python -m primitives.confidence_score.shared.scorer "$f" \
        --threshold medium --format json \
        | jq -r '"  level: \(.level)  score: \(.weighted_score)"'; then
    echo "  GATE BLOCKED: $f" >&2
    FAILED=$((FAILED + 1))
  fi
done

if [ "$FAILED" -gt 0 ]; then
  echo "$FAILED spec(s) below Medium threshold." >&2
  exit 1
fi
echo "All specs passed Medium gate."
```

Run it:

```bash
bash score-all-specs.sh
```

---

## 5. Chaining with F4 /hypothesis

The confidence scorer is designed to pair with F4 `/hypothesis`. After
scaffolding and validating a hypothesis, rate the hypothesis document itself
to confirm it meets the Medium bar before proceeding to implementation.

```bash
# Step 1 — scaffold a hypothesis for lab-2
python -m primitives.hypothesis.shared.scaffolder exercises/lab-2/

# Step 2 — validate the hypothesis against gathered evidence
python -m primitives.hypothesis.shared.validator exercises/lab-2/

# Step 3 — rate the hypothesis.md with F1 before writing any code
python -m primitives.confidence_score.shared.scorer \
  exercises/lab-2/hypothesis.md \
  --threshold medium \
  --context "This hypothesis guides the auth refactor for lab-2."
```

Wiring this chain into the U2 grader rubric (`grader.yaml`):

```yaml
# .forge/grader.yaml
criteria:
  - id: hypothesis-validated
    title: Hypothesis meets Medium confidence bar
    weight: 15
    evidence:
      type: llm-judged
      rubric: |
        The learner must have run /confidence-score on hypothesis.md and
        achieved at least Medium (weighted_score >= 0.40).
        Check that hypothesis.md exists, is non-empty, and contains all
        five standard sections (Hypothesis, Confidence, Falsification,
        Predictions, Null).
      pass_threshold: 0.6
```

The `llm-judged` evidence type delegates scoring to the U2 grader's LLM judge,
which evaluates the rubric text against the file content found in the lab
snapshot — no hard dependency on F1 being present in the scoring environment.
