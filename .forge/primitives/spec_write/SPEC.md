# F5 `/spec-write` — Interview-to-Spec Workflow

## Purpose

`/spec-write` conducts a structured 12-question interview with the developer, then
uses an LLM to draft a six-section `spec.md`, and finally self-reviews the draft
for placeholders, contradictions, ambiguities, and scope issues. The result is a
reviewable, machine-checked specification that guards against vague or incomplete
planning before implementation begins.

**Layer:** L2 Optional — F5

---

## Workflow

```
interview (12 questions, one at a time)
    ↓
draft (LLM fills the six-section spec_template from all 12 answers)
    ↓
self-review (static regex checks + LLM contradiction/ambiguity detection)
    ↓
output (spec.md written to disk; self-review summary printed to stdout)
```

Each step is independent and testable. The interviewer uses `primitives/_llm.py`
`LLMClient` for the question loop. The drafter and self-reviewer also route through
`LLMClient`. Tests use `MockBackend` for full determinism.

---

## Inputs

| Parameter | Type | Default | Description |
|---|---|---|---|
| `target_dir` | path (positional) | `.` | Directory where `spec.md` will be written and where context files are read from |
| `--output` | path | `{target_dir}/spec.md` | Override the output file path |
| `--dry-run` | flag | `false` | Preview the drafted spec on stdout; do **not** write to disk |
| `--backend` | `mock\|bedrock` | `bedrock` | LLM backend. Use `mock` in tests or CI without Bedrock access |

---

## Outputs

### Primary output: `spec.md`

Written to `{target_dir}/spec.md` (or `--output` path) unless `--dry-run` is set.

The file always contains exactly six `##` sections (see [spec_template.md](shared/spec_template.md)):

1. **Goal** — one-sentence goal; who benefits; what is explicitly out of scope
2. **Architecture** — high-level technical approach; key components; data flow
3. **File structure** — new files to create; existing files to modify; deletions
4. **Acceptance criteria** — measurable, falsifiable conditions for "done"
5. **Risks** — failure modes named; mitigations described
6. **Decision log** — decisions already made (with rationale); open decisions for reviewer

### Secondary output: self-review summary (stdout)

After drafting, `self_reviewer.py` prints a summary of any `SelfReviewIssue`
instances found. Issues have a `kind` (one of `placeholder`, `contradiction`,
`ambiguity`, `missing_section`, `scope_creep`) and a human-readable `description`
and `location`.

If the self-review finds no issues, it prints `Self-review: clean.`

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Spec written (or dry-run complete); self-review found no blocking issues |
| 1 | Self-review found one or more issues of kind `placeholder` or `missing_section` (spec written but flagged) |
| 2 | Fatal error (file system, LLM call failure, etc.) |

---

## When to invoke

Invoke `/spec-write` **before starting any non-trivial lab exercise or feature**.
The 12-question interview forces explicit thinking about goal, constraints, failure
modes, file changes, tests, and open decisions before a single line of code is
written.

Typical invocation sequence:

```
/spec-write exercises/lab-3/
# → writes exercises/lab-3/spec.md
# → prints self-review summary

/confidence-score exercises/lab-3/spec.md --threshold medium
# → gates implementation on spec quality
```

---

## Adapter pointer

| Harness | Location |
|---|---|
| Claude Code | `primitives/spec_write/adapters/claude_code/SKILL.md` |
| Copilot | `primitives/spec_write/adapters/copilot/github-bundle/` |

---

## Dependencies

- `primitives/_llm.py` — `LLMClient`, `MockBackend`, `BedrockBackend` (Plan 2)
- `pydantic` v2 — data models
- `pyyaml` — question bank loading
- Standard library: `argparse`, `asyncio`, `pathlib`, `re`

No new third-party dependencies beyond what Plan 2 introduced.
