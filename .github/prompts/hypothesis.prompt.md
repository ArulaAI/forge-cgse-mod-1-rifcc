---
mode: agent
description: Run the Forge F4 /hypothesis primitive — scaffold a new hypothesis.md via 5 guided questions, or validate existing evidence against an existing hypothesis.
---

# /hypothesis

Run the Forge F4 hypothesis primitive on {input:target_dir|.} in {input:mode|scaffold} mode.

## scaffold mode

If `{input:mode|scaffold}` is `scaffold` (or no mode specified):

1. Confirm the target directory: `{input:target_dir|.}`
2. Ask the learner the five hypothesis questions **one at a time**, waiting for each answer before proceeding:
   - **Observation**: What specific behavior or result are you investigating?
   - **Mechanism**: What do you believe is causing it (the "because" statement)?
   - **Predictions**: What measurable outcomes would you expect to see if your hypothesis is correct? (provide at least two)
   - **Null Condition**: What evidence would convince you the hypothesis is wrong?
   - **Confidence**: How confident are you right now — Low, Medium, or High — and why (one sentence)?
3. Once all five answers are collected, run:

```bash
python .forge/primitives/hypothesis/shared/scaffolder.py {input:target_dir|.}
```

   Forward the answers as stdin input in question order.
4. Confirm that `hypothesis.md` has been written. Show a one-sentence summary of the hypothesis (the mechanism claim).
5. Optionally chain to `/confidence-score hypothesis.md --threshold medium` to gate on document quality.

## validate mode

If `{input:mode|scaffold}` is `validate`:

1. Determine the hypothesis file: `{input:hypothesis_file|{input:target_dir|.}/hypothesis.md}`
2. Ask the learner to share their evidence (test output, profiler numbers, git diff, benchmark results — multi-line is fine).
3. Run:

```bash
python .forge/primitives/hypothesis/shared/validator.py {input:hypothesis_file|./hypothesis.md} --evidence "{input:evidence}"
```

4. Surface the support level in uppercase (`SUPPORTED` / `INCONCLUSIVE` / `REFUTED`), the full reasoning paragraph, and any evidence refs.
5. If `REFUTED` (exit code 1): encourage the learner to revise their hypothesis — run `/hypothesis` in scaffold mode.
6. If `INCONCLUSIVE`: encourage gathering more specific evidence before concluding.
7. If `SUPPORTED`: confirm success and suggest chaining to `/confidence-score hypothesis.md --threshold medium`.

## Error handling

If exit code is non-zero for any reason other than `REFUTED` (validate mode), STOP and surface the raw error output — do not attempt to interpret partial results.
