# F4: /hypothesis — Forge primitive contract

## Purpose

Scaffold or validate a `hypothesis.md` for a lab investigation. In `--scaffold` mode the
primitive asks five structured questions one at a time and writes a well-formed hypothesis
document with observation, mechanism, predictions, null condition, and confidence. In
`--validate` mode it reads an existing `hypothesis.md`, scans surrounding evidence (code,
tests, git diff), and reports whether the hypothesis is Supported, Inconclusive, or Refuted.

## Layer

L2 Optional — F4 (Spec A §6.1 — "C: hypothesis-driven development with confidence scoring").

## Inputs

- `target_dir` (positional) — directory that contains (or will contain) `hypothesis.md`.
  Default: current working directory (`.`).
- `--mode` — `scaffold` or `validate`. Required; no default.
- `--hypothesis-file` (optional) — override the default path `{target_dir}/hypothesis.md`.

## Two modes

### `--mode scaffold`

Asks five questions from `shared/questions.yaml` **one at a time**, using the previous answers
as context for each subsequent prompt. Drafts `hypothesis.md` at `{target_dir}/hypothesis.md`
with all five sections populated. Exits 0 on success.

Interactive invocation (Claude Code): the LLM presents each question in turn; the developer
answers in the conversation. The scaffolder collects answers and renders the final file.

### `--mode validate`

Reads the existing `hypothesis.md` at `{target_dir}/hypothesis.md` (or `--hypothesis-file`).
Scans `{target_dir}` for supporting evidence: changed files (`git diff --stat`), test output
summaries, and any `.forge/journey/<run-id>.jsonl` events. Calls the LLM with hypothesis text
+ evidence summary. Emits a validation report to stdout with:

- `support_level`: `supported` | `inconclusive` | `refuted`
- `reasoning`: one paragraph explaining the judgment
- `evidence_refs`: list of files or snippets that drove the verdict

Exits 0 for `supported` or `inconclusive`; exits 1 for `refuted` (allows use as a gate).

## Outputs

| Mode       | Artefact written             | stdout                                        | Exit code |
|------------|------------------------------|-----------------------------------------------|-----------|
| scaffold   | `{target_dir}/hypothesis.md` | Path of written file                          | 0         |
| validate   | *(none)*                     | Validation report (text or JSON)              | 0 / 1     |

## hypothesis.md structure (scaffold output)

```markdown
## Hypothesis

<mechanism claim — the "because" statement>

## Observation

<the specific behavior or result that prompted this investigation>

## Predictions

<what you expect to see if the hypothesis is correct — at least two measurable outcomes>

## Null Condition

<evidence that would convince you the hypothesis is wrong>

## Confidence

<Low | Medium | High> — <one-sentence rationale>
```

## When to invoke

- **Before starting an investigation:** `forge hypothesis --mode scaffold exercises/lab-2/`
  to commit your thinking before reading code.
- **After gathering evidence:** `forge hypothesis --mode validate exercises/lab-2/` to check
  whether what you found supports or refutes your starting hypothesis.
- **Chained with F1:** after `--validate`, run `forge confidence-score hypothesis.md
  --threshold medium` to confirm the hypothesis document itself meets the quality bar.
- **Chained into the U2 grader:** `grader.yaml` can reference a `journey-event-present`
  criterion that checks for a `hypothesis_validated` event, which `--validate` emits when
  it writes to `.forge/journey/`.

## LLM model

Uses the `default` logical model (Bedrock Sonnet via `_llm.py` `BedrockBackend`). Override
with `LLM_BACKEND=mock` for tests.

## Adapters

- Claude Code: `adapters/claude_code/SKILL.md` + `invoke.sh`
- Copilot: `adapters/copilot/SKILL.md` + `github-bundle/skills/hypothesis/SKILL.md`
  + `github-bundle/prompts/hypothesis.prompt.md`
