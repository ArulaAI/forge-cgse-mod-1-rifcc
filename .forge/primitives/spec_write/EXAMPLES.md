# F5 `/spec-write` — Usage Examples

Four real-world patterns for invoking the spec-write primitive in development,
lab exercises, and CI contexts. All examples assume the Forge primitive library
is on `PYTHONPATH` (or installed via `uv`).

---

## 1. Start a lab exercise with `forge spec-write`

Run the full interview-to-spec workflow before writing any code. The primitive
asks 12 questions one at a time, drafts a 6-section `spec.md`, and self-reviews
for placeholders and missing sections.

```bash
# From the lab root — write spec.md into the current directory
python -m primitives.spec_write.shared . --backend bedrock
```

The interviewer prompts each question interactively:

```
Q01: In one sentence: what is the goal of this feature or task?
> Refactor CacheManager.evict() to eliminate a race condition under load.

Q02: What problem does this solve, and for whom?
> Concurrent stress tests fail intermittently; affects lab-2 learners on step 3.

... (10 more questions) ...

Self-review passed — no issues found.
Spec written to /path/to/lab-2/spec.md
```

The resulting `spec.md` contains all six required sections:
`Goal`, `Architecture`, `File structure`, `Acceptance criteria`, `Risks`,
`Decision log`.

To use the mock backend (no Bedrock needed — useful offline or in CI):

```bash
python -m primitives.spec_write.shared . --backend mock
```

---

## 2. Dry-run to preview the drafted spec

Use `--dry-run` to see the drafted spec on stdout without writing it to disk.
Useful for previewing before committing answers or piping to a pager.

```bash
python -m primitives.spec_write.shared . --dry-run --backend bedrock | less
```

The self-review summary still prints to stdout, followed by the full spec text:

```
Self-review found 1 issue(s):
  [placeholder] ## Goal: Section contains an unfilled placeholder comment.

# Spec: Refactor CacheManager.evict()

> **Status:** Draft
> **Author:** Forge Team
> **Date:** 2026-04-18

---

## Goal

<!-- placeholder -->

...
```

Exit code 0 even in dry-run; the caller decides whether to write the file.

To pass a context hint so the interviewer frames questions around your lab:

```bash
python -m primitives.spec_write.shared . \
  --dry-run \
  --backend bedrock \
  --context "lab-3 Python caching exercise — focus on thread safety"
```

---

## 3. Chain F5 with F1 — write spec then gate on confidence

Run the full spec-write workflow, then immediately score the resulting
`spec.md` with the F1 confidence scorer before writing any implementation code.
The chain exits non-zero if either step fails.

```bash
# Step 1 — interview and draft
python -m primitives.spec_write.shared exercises/lab-2/ --backend bedrock

# Step 2 — gate the spec at Medium confidence before writing code
python -m primitives.confidence_score.shared.scorer \
  exercises/lab-2/spec.md \
  --threshold medium \
  --context "spec.md written by F5 spec-write for lab-2 cache refactor"
```

Sample output from Step 2 when the gate passes:

```
Confidence level : HIGH
Weighted score   : 0.7820
Gate passed      : True

  [specificity]            0.90 — States scope and non-goals clearly.
  [error_handling]         0.75 — Two failure modes named explicitly.
  [testability]            0.85 — Each criterion is falsifiable.
  [dependency_clarity]     0.72 — Existing deps only; no new packages.
  [security_consideration] 0.70 — Thread-safety risk noted in Risks section.
```

Wire the chain into a single CI step:

```bash
#!/usr/bin/env bash
set -euo pipefail
TARGET="exercises/lab-2"

python -m primitives.spec_write.shared "$TARGET" --backend bedrock
python -m primitives.confidence_score.shared.scorer "$TARGET/spec.md" \
  --threshold medium

echo "Spec written and confidence gate passed."
```

---

## 4. Using the Copilot adapter in VS Code Chat

The Copilot adapter ships a `.prompt.md` that turns VS Code Copilot Chat into
an F5 interviewer. No CLI invocation needed — the interviewer runs inline as a
series of chat turns, then calls the primitive to draft and self-review.

### Setup

Copy the prompt bundle into the lab workspace:

```bash
cp -r .forge/primitives/spec_write/adapters/copilot/github-bundle/.github .
```

The bundle registers the `/spec-write` prompt in Copilot Chat.

### Running the workflow in Chat

1. Open VS Code in the lab root.
2. Open Copilot Chat (`Ctrl+Shift+I` / `Cmd+Shift+I`).
3. Type `/spec-write` (or `/spec-write exercises/lab-2/` to target a specific
   directory).
4. Answer each of the 12 questions as Copilot asks them — one per chat turn.
5. Copilot drafts `spec.md`, surfaces any self-review issues inline as
   `<!-- TODO: ... -->` comments, and confirms the file path.

The Copilot adapter uses the mock backend by default so no AWS credentials are
required in the IDE session. Switch to `--backend bedrock` by editing
`spec-write.prompt.md` line 35 if Bedrock is available.

### Self-review issue surfacing

When self-review finds issues, Copilot inserts structured comments at the
relevant spec locations:

```markdown
<!-- TODO: [placeholder] at ## Goal — Section contains an unfilled placeholder. -->
```

Resolve each comment, then re-run `/spec-write` or edit `spec.md` directly.
After resolution, optionally chain to F1:

```
/confidence-score exercises/lab-2/spec.md --threshold medium
```
