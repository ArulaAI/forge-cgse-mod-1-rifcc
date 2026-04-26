---
name: hypothesis
description: Scaffold a structured hypothesis.md via 5 guided questions, or validate existing evidence against a hypothesis. Invoke before writing implementation code (scaffold) or after gathering test/profiler/diff evidence (validate).
---

# /hypothesis

Claude Code adapter for the Forge primitive library F4 primitive.

## When invoked

### Scaffold mode

Use when the learner wants to articulate a new hypothesis before implementing a fix or experiment.

1. Determine the target directory — user-mentioned path, else `.`
2. Determine the LLM backend — user-supplied `--backend bedrock|mock`, else `bedrock`
3. Run: `bash <skill_dir>/invoke.sh --scaffold <target_dir> [--backend <backend>]`
4. The script will prompt for 5 answers interactively via stdin. Surface each question to the user and forward their answer.
5. On success (exit 0), confirm that `hypothesis.md` has been written to the target directory.

### Validate mode

Use when the learner has gathered evidence (test results, profiler output, code diffs, benchmark numbers) and wants to evaluate whether it supports their hypothesis.

1. Determine the hypothesis file path — user-mentioned path or `./hypothesis.md`
2. Collect the evidence text from the user (multi-line is fine)
3. Determine the LLM backend — user-supplied `--backend bedrock|mock`, else `bedrock`
4. Run: `bash <skill_dir>/invoke.sh --validate <hypothesis_file> --evidence "<evidence_text>" [--backend <backend>]`
5. Parse output. Surface the support level (`SUPPORTED` / `INCONCLUSIVE` / `REFUTED`), reasoning, and evidence refs.
6. If `REFUTED`, encourage the learner to revisit their hypothesis using `--scaffold`.
7. If `INCONCLUSIVE`, encourage gathering more specific evidence.

## Output expectations

- **Scaffold**: Confirm path written and show a one-sentence summary of the hypothesis.
- **Validate**: Always surface the support level in uppercase, the full reasoning paragraph, and any evidence refs.

## Invariants

- Logic lives in `primitives/hypothesis/shared/scaffolder.py` and `validator.py` in the Forge primitive library.
- DO NOT modify `invoke.sh` or duplicate hypothesis logic — primitive library upgrades flow through `forge sync`.

## Usage examples

```bash
# Scaffold a new hypothesis into the current working directory
bash .forge/primitives/hypothesis/adapters/claude_code/invoke.sh --scaffold .

# Scaffold into a specific feature directory
bash .forge/primitives/hypothesis/adapters/claude_code/invoke.sh --scaffold src/features/query-cache

# Validate evidence against an existing hypothesis
bash .forge/primitives/hypothesis/adapters/claude_code/invoke.sh \
  --validate src/features/query-cache/hypothesis.md \
  --evidence "Benchmark shows p95 latency dropped from 340 ms to 82 ms after adding LRU cache."
```
