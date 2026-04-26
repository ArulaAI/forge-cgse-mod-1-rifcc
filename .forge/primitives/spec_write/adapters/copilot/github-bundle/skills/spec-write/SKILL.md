---
name: spec-write
description: Interview-to-spec workflow. Asks 12 questions one at a time, drafts a 6-section spec.md, self-reviews for placeholders/contradictions/scope. Invoke at the start of any non-trivial lab exercise before writing code.
mode: agent
tools:
  - shell
  - filesystem
---

# Skill: spec-write

Conduct a structured 12-question interview with the developer, draft a six-section `spec.md`, and self-review the draft for placeholders, contradictions, ambiguities, and scope issues.

## How to invoke

Ask the developer the 12 interview questions **one at a time** (each in a separate turn), collect all answers, then run:

```bash
python .forge/primitives/spec_write/shared/__main__.py {input:target_dir|.} --backend mock
```

Or use the slash command `/spec-write` from `prompts/spec-write.prompt.md`.

## 12 interview questions (in order)

Ask these one at a time, waiting for each answer before proceeding:

1. In one sentence: what is the goal of this feature or task?
2. What problem does this solve, and for whom?
3. What are the non-negotiable constraints? (tech stack, existing APIs, performance budget, etc.)
4. How will you know when this is done? Give at least two measurable acceptance criteria.
5. What could go wrong? Name at least two failure modes this design must handle.
6. What is your high-level technical approach in 2-4 sentences?
7. Which existing files will be modified, and which new files will be created?
8. What tests will you write to verify correctness?
9. What is the biggest risk in this plan, and how will you mitigate it?
10. What external dependencies does this introduce? Any new packages or services?
11. What decisions have already been made that this plan must respect?
12. What decisions are still open that a reviewer should weigh in on?

## Six-section spec structure

The generated `spec.md` always contains exactly these sections:

1. **Goal** — one-sentence goal; who benefits; what is explicitly out of scope
2. **Architecture** — high-level technical approach; key components; data flow
3. **File structure** — new files to create; existing files to modify; deletions
4. **Acceptance criteria** — measurable, falsifiable conditions for "done"
5. **Risks** — failure modes named; mitigations described
6. **Decision log** — decisions already made (with rationale); open decisions for reviewer

## Self-review output

After drafting, self-review findings are printed to stdout. If blocking issues (`placeholder` or `missing_section` kind) are found, surface them as `<!-- TODO: ... -->` inline comments at the relevant location in `spec.md` and list them as structured action items for the developer to resolve before proceeding.

Exit code 1 means blocking issues were found — state clearly that the spec needs revision before implementation starts.

## Invariants

- Logic lives in `.forge/primitives/spec_write/shared/` — DO NOT duplicate interviewer/drafter/self-reviewer logic here
- Updates land via `forge sync` per the lab's `.forge/manifest.yaml` pin
- `mode: agent` is required so Copilot can run the multi-turn 12-question interview loop
