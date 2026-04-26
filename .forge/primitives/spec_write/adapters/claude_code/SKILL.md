---
name: spec-write
description: Interview-to-spec workflow. Asks 12 questions one at a time, drafts a 6-section spec.md, self-reviews for placeholders/contradictions/scope. Invoke at the start of any non-trivial lab exercise before writing code.
---

# /spec-write

Claude Code adapter for the Forge primitive library F5 primitive.

## When invoked

1. Determine the target directory — user-mentioned path, else `.`
2. Determine the output path — user-supplied `--output <path>`, else `{target_dir}/spec.md`
3. Determine the backend — user-supplied `--backend mock|bedrock`, else `bedrock`
4. Run: `bash <skill_dir>/invoke.sh [target_dir] [--output <path>] [--dry-run] [--backend <backend>] [--context <text>]`
5. The primitive will ask 12 interview questions one at a time; relay each question to the user and pass each answer back through the script (or let the LLM backend drive the interview in autonomous mode).
6. Parse output. On exit code 1, surface the self-review issues as structured action items and recommend the developer address placeholders/missing sections before proceeding.

## Output expectations

- Always surface the final spec.md path on success
- Show self-review results: either "Self-review passed — no issues found." or a structured list of issues with kind, location, and description
- On exit code 1 (blocking issues found), state clearly that the spec has placeholders or missing sections and recommend the developer resolve them before starting implementation
- On exit code 0, confirm the spec is ready and encourage proceeding to implementation

## Invariants

- Logic lives in `primitives/spec_write/shared/` in the Forge primitive library
- DO NOT modify `invoke.sh` or duplicate interviewer/drafter/self-reviewer logic — primitive library upgrades flow through `forge sync`

## Six-section spec structure

The generated `spec.md` always contains exactly these sections:

1. **Goal** — one-sentence goal; who benefits; what is explicitly out of scope
2. **Architecture** — high-level technical approach; key components; data flow
3. **File structure** — new files to create; existing files to modify; deletions
4. **Acceptance criteria** — measurable, falsifiable conditions for "done"
5. **Risks** — failure modes named; mitigations described
6. **Decision log** — decisions already made (with rationale); open decisions for reviewer
