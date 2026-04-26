# Primitive tour — `forge-cgse-mod-1-rifcc`

## L1 — Lab-specific

| Primitive | Path |
|---|---|
| `rifcc-walker` agent (Claude/Copilot) | `.claude/agents/rifcc-walker.md`, `.github/agents/rifcc-walker.agent.md` |
| Educator output style | `.claude/output-styles/educator.md` |
| `/walk-rifcc`, `/critique-prompts` | `.claude/commands/`, `.github/prompts/` |
| RIFCC rule (Claude/Copilot) | `.claude/rules/rifcc.md`, `.github/instructions/rifcc.instructions.md` |

### Net-new 2026-04-25 capabilities

claude-agent-mcp-servers (empty — RIFCC is prompt-only), claude-agent-hooks-frontmatter, claude-agent-permission-mode, claude-output-styles, claude-plan-mode-doc, copilot-coding-agent, copilot-mcp-allowlist.

## L2 — Synced

7 primitives at `.forge/primitives/`.

## L3 — `/walk-rifcc` (canonical F8)

`.forge/local/primitives/walk-rifcc/` — pure-stdlib walker. 5 pytest cases. Also published
upstream to `arula-ai/forge-prowess-primitives/primitives/walk_rifcc/` so every other lab can
sync it.
