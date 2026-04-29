---
mode: agent
description: Run the Forge F1 /confidence-score primitive on an artifact.
---

# /confidence-score

Rate {input:target|.} for confidence against the 5-dimension Forge rubric.

If no target provided, default to current working directory (`.`).

Run:

```bash
python .forge/primitives/confidence_score/shared/scorer.py {input:target|.} --threshold {input:threshold|medium} --format markdown
```

Surface the final confidence level (Low / Medium / High) and the weighted score. For each dimension, show the dimension name, per-dimension score, and one-sentence reasoning.

If `gate_passed` is false (exit code 1), state clearly:
- Which threshold was required and what level was scored
- Which dimensions scored lowest
- A concrete recommendation for what the learner should add or clarify to raise those dimensions before proceeding

If `gate_passed` is true (exit code 0), confirm success and encourage the learner to proceed with implementation.

If exit code is non-zero for any other reason, STOP and surface the raw error output — do not attempt to interpret partial results.
