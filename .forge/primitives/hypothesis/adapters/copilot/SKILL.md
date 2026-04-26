# /hypothesis — GitHub Copilot adapter

Copilot-side counterpart to the Claude Code adapter. Both share `shared/scaffolder.py` and `shared/validator.py`.

## What lands in a lab repo

When `forge sync` runs in a lab, contents of `github-bundle/` merge into the lab's `.github/`:

- `.github/skills/hypothesis/SKILL.md` — the actual Copilot skill manifest
- `.github/prompts/hypothesis.prompt.md` — slash-command prompt for direct invocation

The lab's `.github/copilot-instructions.md` (thin) cross-references both.
