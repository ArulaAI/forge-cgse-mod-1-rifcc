# F1: /confidence-score — Forge primitive contract

## Purpose

Rate any artifact (code file, spec, hypothesis, prompt) Low/Medium/High confidence using a
rubric-driven LLM judge. Optionally gate downstream steps — blocks "implement now" until the
artifact reaches the configured threshold.

## Layer

L2 Optional — F1 (Spec A §6.1 — "C: hypothesis-driven development with confidence scoring").

## Inputs

- `target` (positional) — path to the file to score, or `-` to read from stdin.
- `--context` (optional) — free-text describing the task or intent; injected into the LLM prompt
  to anchor evaluation. Example: `"This is a spec for the auth module."`.
- `--threshold` (optional) — gate level: `low`, `medium`, or `high`. Exit code 1 when the
  artifact scores *below* this threshold. Default: `medium`.
- `--format` (optional) — `text` (default, human-readable) or `json`.

## Outputs

- **stdout:** score level, per-dimension reasoning, and overall weighted score.
  - `text` format: readable prose with one line per dimension.
  - `json` format: object with keys `score` (`"low"` | `"medium"` | `"high"`), `reasoning`
    (string), and `criteria_evaluated` (list of `{id, score, reasoning}` objects).
- **exit code:**
  - `0` — artifact is at or above `--threshold` (gate passed, or no gate configured).
  - `1` — artifact is below `--threshold` (gate blocked) or an unrecoverable error occurred.

## Gate semantics

When `--threshold` is set (default: `medium`), the scorer raises `GateBlockedError` in library
mode or exits with code `1` in CLI mode if `weighted_score < threshold_floor`. This is the
canonical **confidence gate** referenced in Spec A §6.1 — the same pattern used by U1's
`--max-severity` flag applied to hypothesis-driven development.

Default threshold floor values (from `shared/rubric.yaml`):

| Level  | Weighted score range |
|--------|---------------------|
| Low    | 0.00 – 0.39         |
| Medium | 0.40 – 0.69         |
| High   | 0.70 – 1.00         |

## When to invoke

- **Before implementation:** rate a spec or design doc before writing any code.
- **Before committing a spec:** gate PRs on spec quality (`forge confidence-score spec.md`).
- **Inside a `PreToolUse` hook:** intercept Write/Edit events and score the about-to-be-written
  artifact when `--threshold high` is required by the lab config.
- **Chained with F4 /hypothesis:** after `/hypothesis --validate`, score the hypothesis doc
  itself to confirm it meets the Medium bar before proceeding.

## LLM model

Uses the `default` logical model (maps to Bedrock Sonnet in the primitive library's `_llm.py`
`BedrockBackend`). Override via the `LLM_BACKEND` env var to `mock` for tests.

## Scoring rubric

Five dimensions defined in `shared/rubric.yaml`. Weights sum to 1.0:

| Dimension            | Weight | Description                                               |
|----------------------|--------|-----------------------------------------------------------|
| specificity          | 0.25   | Artifact states what it does and what it does NOT do      |
| error_handling       | 0.20   | Failure paths explicitly addressed                        |
| testability          | 0.25   | Acceptance criteria are measurable and falsifiable        |
| dependency_clarity   | 0.15   | External dependencies named and versions constrained      |
| security_consideration | 0.15 | Security-relevant inputs or outputs explicitly noted      |

## Adapters

- Claude Code: `adapters/claude_code/SKILL.md` + `invoke.sh`
- Copilot: `adapters/copilot/SKILL.md` + `github-bundle/skills/confidence-score/SKILL.md`
  + `github-bundle/prompts/confidence-score.prompt.md`
