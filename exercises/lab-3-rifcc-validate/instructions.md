---
lesson_id: cgse-mod-1::lab-3-rifcc-validate
estimated_min: 25
workflows: [W3]
failure_modes: [FM2, FM4]
mode: validate
---

# Lab 3 — Validate RIFCC outputs

**Why this matters.** A walked prompt only earns its keep if the LLM's response actually clears
the acceptance bar. This is where you catch the "looked structured, still hallucinated" failures
— and where FM4 (context loss across multi-step work) shows up most often.

Send each of the lab-2 walked prompts to an LLM. Compare the responses against acceptance
criteria written in `spec.md`. Capture FM4 (context loss) findings.

## Acceptance criteria

- ≥ 5 LLM responses validated against spec.
- `confidence_score` medium/high.
