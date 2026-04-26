---
name: hypothesis
description: Scaffold a structured hypothesis.md via 5 guided questions (scaffold mode), or validate existing evidence against a hypothesis (validate mode). Invoke before implementing a fix to articulate your thinking, or after gathering evidence to check if your hypothesis holds.
tools:
  - shell
---

# Skill: hypothesis

Scaffold or validate a `hypothesis.md` for a lab investigation.

## Modes

### scaffold

Ask five structured questions one at a time (observation, mechanism, predictions, null condition, confidence). Write a well-formed `hypothesis.md` at `{target_dir}/hypothesis.md`.

Run:

```bash
python .forge/primitives/hypothesis/shared/scaffolder.py {input:target_dir|.}
```

Present each question from `shared/questions.yaml` to the learner in turn, collect their answers interactively, and forward them to the scaffolder. On exit 0, confirm the file path written and show a one-sentence summary of the hypothesis.

### validate

Read the existing `hypothesis.md` at `{target_dir}/hypothesis.md` (or a user-supplied path). Gather evidence text from the learner (test results, profiler output, diffs, benchmark numbers). Pass hypothesis + evidence to the validator.

Run:

```bash
python .forge/primitives/hypothesis/shared/validator.py {input:hypothesis_file|./hypothesis.md} --evidence "{input:evidence}"
```

Surface the support level (`SUPPORTED` / `INCONCLUSIVE` / `REFUTED`), the reasoning paragraph, and any evidence refs.

- `REFUTED` — encourage the learner to revisit their hypothesis using scaffold mode.
- `INCONCLUSIVE` — encourage gathering more specific evidence.

## Invocation pattern

Use `{input:mode|scaffold}` to select the mode. Default is `scaffold` when the learner has not yet written a hypothesis; switch to `validate` when evidence has been gathered.

## Chaining

After `--validate`, optionally chain to `/confidence-score hypothesis.md --threshold medium` to confirm the document itself meets the quality bar (F1 primitive).

## Invariants

- Logic lives in `shared/scaffolder.py` and `shared/validator.py` — DO NOT duplicate hypothesis logic here.
- Updates land via `forge sync` per the lab's `.forge/manifest.yaml` pin.
- `mode: agent` is required so Copilot can run the multi-turn question loop for scaffold mode.
