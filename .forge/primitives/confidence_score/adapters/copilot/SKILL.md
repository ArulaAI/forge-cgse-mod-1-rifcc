# /confidence-score — GitHub Copilot adapter

Copilot-side counterpart to the Claude Code adapter. Both share `shared/scorer.py`.

## What lands in a lab repo

When `forge sync` runs in a lab, contents of `github-bundle/` merge into the lab's `.github/`:

- `.github/skills/confidence-score/SKILL.md` — the actual Copilot skill manifest
- `.github/prompts/confidence-score.prompt.md` — slash-command prompt for direct invocation

The lab's `.github/copilot-instructions.md` (thin) cross-references both.
