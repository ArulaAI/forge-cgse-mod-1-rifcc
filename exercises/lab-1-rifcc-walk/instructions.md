---
lesson_id: cgse-mod-1::lab-1-rifcc-walk
estimated_min: 25
workflows: [W3]
failure_modes: [FM2, FM4]
mode: analyze
---

# Lab 1 — Walk a fuzzy ask through RIFCC

**Why this matters.** Most "AI says my refactor is fine" moments come from prompts that never
named the Role, scoped the Frame, or set Constraints. The walk turns a 5-second fuzzy ask into a
60-second structured one — and that 60 seconds is what stops you from merging code on vibes.

Take a fuzzy ask ("review my refactor") and walk it through R-I-F-C-C using `/walk-rifcc`.
Capture the structured prompt in `spec.md`.

## Acceptance criteria

- `walk_rifcc_run` event with `letters_walked >= 5`.
- `confidence_score` medium/high.
