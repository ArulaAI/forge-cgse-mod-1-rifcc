# F4 `/hypothesis` — Usage Examples

Five real-world patterns for invoking the hypothesis primitive in development,
lab exercises, and CI contexts. All examples assume the Forge primitive library
is on `PYTHONPATH` (or installed via `uv`).

---

## 1. Scaffold a hypothesis before starting a lab exercise

Form your thinking *before* reading the code. Running `--scaffold` first
forces you to commit to a mechanism claim you can later prove or refute.

```bash
# From the lab root — scaffold a hypothesis for lab-2
python -m primitives.hypothesis.shared.scaffolder exercises/lab-2/
```

The scaffolder asks five questions one at a time, elaborates each answer with
the LLM, and writes `exercises/lab-2/hypothesis.md`:

```
Q1: What specific behavior or result did you observe?
> I noticed the cache invalidation fails intermittently under load.

Q2: What mechanism do you think explains the observation?
> A race condition in CacheManager.evict() causes a double-free.

Q3: What do you predict will happen if your hypothesis is correct?
> Adding a lock should eliminate the AssertionError under stress tests.

Q4: What evidence would convince you the hypothesis is wrong?
> If single-threaded tests also fail, the hypothesis is refuted.

Q5: How confident are you right now, and why?
> Medium — plausible but not yet proven under a controlled scheduler.

hypothesis.md written to: exercises/lab-2/hypothesis.md
```

The resulting `hypothesis.md` contains all five sections:
`Hypothesis`, `Mechanism`, `Predictions`, `Null Condition`, `Confidence`.

To use the mock backend (no Bedrock needed — useful in CI):

```bash
python -m primitives.hypothesis.shared.scaffolder exercises/lab-2/ --backend mock
```

---

## 2. Validate a hypothesis after gathering evidence

Run `--validate` after applying a patch and re-running tests. The primitive
reads your `hypothesis.md`, accepts your evidence description, and classifies
the outcome as `SUPPORTED`, `INCONCLUSIVE`, or `REFUTED`.

```bash
python -m primitives.hypothesis.shared.validator \
  exercises/lab-2/hypothesis.md \
  --evidence "Lock patch applied to CacheManager.evict(). Stress test now passes
  with 16 workers over 1000 iterations. Single-threaded run never failed (as
  predicted). No new test failures." \
  --backend bedrock
```

Sample output when the evidence supports the hypothesis:

```
Support level : SUPPORTED
Reasoning     : The stress test regression confirms the race condition: adding the
                lock eliminated all observed failures, and the single-threaded run
                continued to pass as predicted by the null condition.
Evidence refs : starter/cache_manager.py:84-102, starter/test_stress.py
```

Sample output when the evidence refutes it:

```
Support level : REFUTED
Reasoning     : Single-threaded test also fails consistently, ruling out the race
                condition. The off-by-one allocation hypothesis is now more likely.
Evidence refs : starter/test_stress.py
```

The validator exits 1 on `refuted`, making it usable as a CI gate:

```bash
python -m primitives.hypothesis.shared.validator hypothesis.md \
  --evidence "$(cat test_output.txt)" \
  || echo "Hypothesis refuted — revisit your mechanism claim."
```

---

## 3. JSON output piped to `jq`

Both the scaffolder (after writing the file) and the validator emit
machine-readable output when combined with Python's `-c` flag or when the
validator result is serialised. Use `jq` to extract specific fields.

```bash
# Validate and extract just the support level
python -c "
import json
from pathlib import Path
from primitives.hypothesis.shared.validator import validate
from primitives._llm import BedrockBackend
result = validate(
    hypothesis_file=Path('exercises/lab-2/hypothesis.md'),
    evidence_text='Patch applied; stress test passes.',
    llm_backend=BedrockBackend(),
)
print(json.dumps({
    'support_level': result.support_level,
    'reasoning': result.reasoning,
    'evidence_refs': result.evidence_refs,
}))
" | jq '.support_level'
```

Output:

```json
"supported"
```

Full JSON shape:

```json
{
  "support_level": "supported",
  "reasoning": "Evidence clearly confirms the hypothesis.",
  "evidence_refs": ["starter/cache_manager.py:84", "starter/test_stress.py"]
}
```

Extract the reasoning only:

```bash
... | jq -r '.reasoning'
```

Check that at least one evidence ref was cited:

```bash
... | jq 'if (.evidence_refs | length) > 0 then "refs present" else error("no refs") end'
```

---

## 4. Pairing with F1 `/confidence-score` (scaffold → validate → gate)

Chain F4 with F1 to enforce quality at every stage: score the hypothesis
document *before* writing code, and re-score after validation.

```bash
# Step 1 — scaffold hypothesis before touching any code
python -m primitives.hypothesis.shared.scaffolder exercises/lab-2/ --backend bedrock

# Step 2 — gather evidence (run tests, apply patch, read diff)
git diff HEAD starter/ > /tmp/patch.txt

# Step 3 — validate the hypothesis against your evidence
python -m primitives.hypothesis.shared.validator exercises/lab-2/hypothesis.md \
  --evidence "$(cat /tmp/patch.txt)" --backend bedrock

# Step 4 — gate the hypothesis.md with F1 at Medium confidence
python -m primitives.confidence_score.shared.scorer \
  exercises/lab-2/hypothesis.md \
  --threshold medium \
  --context "Hypothesis for the cache race condition in lab-2."
```

Sample output from Step 4 when the gate passes:

```
Confidence level : HIGH
Weighted score   : 0.7820
Gate passed      : True

  [specificity]           0.90 — States scope and non-goals clearly.
  [error_handling]        0.75 — Null condition is explicit.
  [testability]           0.85 — Two measurable predictions listed.
  [dependency_clarity]    0.72 — References specific files and line ranges.
  [security_consideration] 0.70 — Race condition identified as the root risk.
```

Wire the chain into `.claude/settings.json` so Claude Code auto-gates
hypothesis writes:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$CLAUDE_TOOL_INPUT_FILE_PATH\" | grep -q hypothesis.md && python -m primitives.confidence_score.shared.scorer \"$CLAUDE_TOOL_INPUT_FILE_PATH\" --threshold medium || true'"
          }
        ]
      }
    ]
  }
}
```

---

## 5. Chaining into the U2 grader as an `llm-judged` criterion

Include hypothesis validation as a graded rubric criterion. The `llm-judged`
evidence type lets the grader's LLM evaluate whether the learner produced and
validated a high-quality hypothesis, without hard-wiring F4 into the grading
environment.

```yaml
# .forge/grader.yaml
criteria:
  - id: hypothesis-present
    title: Hypothesis document scaffolded before implementation
    weight: 10
    evidence:
      type: file-exists
      path: hypothesis.md

  - id: hypothesis-quality
    title: Hypothesis meets Medium confidence bar (F1 gate)
    weight: 15
    evidence:
      type: llm-judged
      rubric: |
        The learner must have scaffolded a hypothesis.md that contains all five
        sections: Hypothesis, Mechanism, Predictions, Null Condition, Confidence.
        Each section must be non-empty and technically specific. The Predictions
        section must include at least two measurable outcomes. The Null Condition
        must describe evidence that would refute the hypothesis.
        Pass threshold: at least 4 of 5 sections are well-formed and specific.
      pass_threshold: 0.6

  - id: hypothesis-validated
    title: Hypothesis validated against evidence after investigation
    weight: 15
    evidence:
      type: llm-judged
      rubric: |
        The learner must have run forge hypothesis --validate on hypothesis.md
        and obtained a result of 'supported' or 'inconclusive'. Evidence for this
        is the presence of a validation summary in journey.jsonl (event type
        'hypothesis_validated') or a written commentary explaining the outcome.
        A 'refuted' result is acceptable if the learner documented a revised
        hypothesis and re-ran validation. A missing validation earns 0 points.
      pass_threshold: 0.6
```

To also use the `journey-event-present` evidence type (when the grader has
access to `.forge/journey/`):

```yaml
  - id: hypothesis-event
    title: hypothesis_validated event logged in journey
    weight: 5
    evidence:
      type: journey-event-present
      event_type: hypothesis_validated
```

The `journey-event-present` criterion requires the validator to emit a
`hypothesis_validated` event to `.forge/journey/<run-id>.jsonl`. This happens
automatically when `--validate` succeeds and the journey recorder is active.
