---
mode: agent
description: Run the Forge F5 /spec-write primitive — interview the developer with 12 questions, draft a 6-section spec.md, and self-review for placeholders and missing sections.
---

# /spec-write

Conduct the Forge F5 spec-write workflow for {input:target_dir|.}.

## Step 1: Interview (12 questions, one per turn)

Ask each of the following questions **one at a time**, waiting for the developer's answer before moving to the next. Do NOT ask multiple questions in a single message.

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

## Step 2: Draft the spec

Once all 12 answers are collected, run:

```bash
python .forge/primitives/spec_write/shared/__main__.py {input:target_dir|.} --backend mock
```

Forward the answers as stdin input in question order (q01 through q12).

## Step 3: Self-review and surface issues

After the primitive exits:

- On exit code 0: confirm that `spec.md` has been written to `{input:target_dir|.}/spec.md`. Show the self-review summary ("Self-review: clean." or the list of issues found).
- On exit code 1 (blocking issues found):
  - State clearly: the spec has placeholder or missing-section issues that must be resolved before implementation begins.
  - For each `SelfReviewIssue` of kind `placeholder` or `missing_section`, surface it as an inline comment at the relevant spec location:
    ```
    <!-- TODO: [kind] at [location] — [description] -->
    ```
  - List all issues as structured action items with `kind`, `location`, and `description`.
  - Recommend the developer address each `<!-- TODO: ... -->` comment and re-run `/spec-write` or edit `spec.md` directly.
- On exit code 2 (fatal error): STOP and surface the raw error output — do not attempt to interpret partial results.

## Chaining

After a clean spec, optionally chain to `/confidence-score {input:target_dir|.}/spec.md --threshold medium` (F1 primitive) to gate implementation on spec quality.
