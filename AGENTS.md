# AGENTS.md — forge-cgse-mod-1-rifcc

A junior dev pings #engineering: "AI says my refactor is fine — should I merge?" The answer
depends on whether the prompt set the **R**ole (reviewer? author?), the **I**ntent (find bugs?
verify spec?), the **F**rame (which files? what scope?), the **C**onstraints (no rewrites? no
new deps?), and the **C**onfidence rating (what would change "yes" to "no"). This lab teaches
RIFCC — the prompt-engineering pattern that turns "AI says fine" into a structured artifact.

## Build / test / run

```bash
uv sync
make demo                       # entry-point hint
make test                       # uv run pytest (L3 + smoke)
make grade                      # make test + L2 lab-grader
make sync                       # forge sync — refresh .forge/primitives/
make validate                   # forge validate .
```

## Project invariants

- `spec.md` populated (status: ≠ draft) before touching `starter/`
- `hypothesis.md` confidence ≥ Medium before implementation
- `.forge/manifest.yaml` pins `forge_primitives_version: "0.4.0"`
- L3 primitives at `.forge/local/primitives/walk-rifcc/` (canonical F8 reference impl)
- All agents in `.claude/agents/` carry `mcpServers:`, `hooks:`, `permissionMode:` frontmatter
- The **rifcc-walker** sub-agent uses Educator output style; mandatory
- Every prompt must walk RIFCC (R-I-F-C-C) before being sent to an LLM
- `exercises/*/reference/` is NEVER modified

## Where things live

- `cgse-lab1-angular/`, `cgse-lab1-java/` — preserved language-specific samples
- `docs/` — preserved CGSE docs
- `exercises/` — 4 modernized labs (lab-1-rifcc-walk, lab-2-rifcc-batch, lab-3-rifcc-validate, lab-4-critique-prompts)
- `.forge/local/primitives/walk-rifcc/` — canonical F8 `/walk-rifcc` primitive (also published upstream)

## AI agent guidance

1. Always run `/walk-rifcc` before sending any non-trivial prompt to an LLM.
2. Surface FM2 (overly-broad asks) and FM4 (context loss across multi-step work).
3. Never modify `exercises/*/reference/`.
4. End every Educator-style response with `**Confidence:** Low / Medium / High — <rationale>`.

## What to read

- `docs/overview.md`, `docs/primitive-tour.md`
- [Plan 16](https://github.com/arula-ai/forge-prowess-labs-modernization/blob/master/docs/superpowers/plans/2026-04-25-plan-16-cgse-mod-1-rifcc-modernization.md)
