# Spec: <!-- One-line title matching the q01_goal answer -->

> **Status:** Draft — pending self-review  
> **Author:** <!-- Developer name or team -->  
> **Date:** <!-- ISO date YYYY-MM-DD -->

---

## Goal

<!-- State the single goal of this feature or task in one sentence.
     Include who benefits and what is explicitly OUT of scope.
     Source: q01_goal + q02_problem answers. -->

---

## Architecture

<!-- Describe the high-level technical approach in 2-5 sentences.
     Name the key components, their responsibilities, and the data flow between them.
     Include a Mermaid diagram if the flow is non-trivial.
     Source: q06_approach + q10_dependencies answers. -->

---

## File structure

<!-- List every file that will be CREATED or MODIFIED by this task.
     Use a fenced code block with the tree layout. Mark new files with (NEW) and
     modified files with (MOD). Include deletions if any.
     Source: q07_files answer. -->

```
<repo-root>/
  <path/to/new_file.py>         # (NEW) — brief one-line description
  <path/to/existing_file.py>    # (MOD) — what changes
```

---

## Acceptance criteria

<!-- List at least two measurable, falsifiable conditions for "done".
     Each criterion must be independently verifiable (automated test or manual check).
     Prefix each with "[ ]" so it can be checked off.
     Source: q04_success + q08_tests answers. -->

- [ ] <!-- Criterion 1: specific, observable outcome -->
- [ ] <!-- Criterion 2: specific, observable outcome -->

---

## Risks

<!-- Name the failure modes this design must handle (from q05_failure_modes)
     and the biggest risk with its mitigation (from q09_risks).
     Use a table or bulleted list. -->

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <!-- failure mode 1 --> | <!-- Low/Med/High --> | <!-- Low/Med/High --> | <!-- how handled --> |
| <!-- failure mode 2 --> | <!-- Low/Med/High --> | <!-- Low/Med/High --> | <!-- how handled --> |

---

## Decision log

<!-- Two sub-sections: decisions already locked in (from q11_decided) and
     decisions still open for reviewer input (from q12_open). -->

### Decided

<!-- List decisions that are already made and must not be re-litigated.
     Include a one-sentence rationale for each. -->

- <!-- Decision 1: rationale -->

### Open

<!-- List decisions the reviewer should weigh in on before implementation starts.
     Frame each as a question with 2-3 candidate answers if possible. -->

- <!-- Open question 1: [Option A | Option B | Other] -->
