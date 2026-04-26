# Copilot Instructions — forge-cgse-mod-1-rifcc

This repo follows the dual-harness AGENTS.md pattern. **`AGENTS.md` is canonical**.

## Copilot-specific deltas

- Mode dropdown contains the **`rifcc-walker`** agent.
- 2 prompts via `/`: `/walk-rifcc`, `/critique-prompts`.
- Path-scoped instructions in `.github/instructions/rifcc.instructions.md` (`applyTo: **/*.md`) auto-attach.
- MCP allowlist with **Copilot Coding Agent** enabled (`codingAgentEnabled: true`); RIFCC is prompt-engineering only — no MCP servers required.

## Journey recorder hook

Runs automatically via `.github/hooks/hooks.json`.

## Running commands

Prefer Copilot Chat's `#runInTerminal` for the lab's make targets so each invocation is captured
in the journey recorder:

- `#runInTerminal make demo`
- `#runInTerminal make test`
- `#runInTerminal make grade`
- `#runInTerminal make validate`

## Validation

`forge validate .` from repo root before opening a PR.
