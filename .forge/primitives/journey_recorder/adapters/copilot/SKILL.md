---
name: journey-recorder
description: Always-on hook adapter that records Copilot lifecycle events (pre-request, post-response — plus sessionStart/sessionEnd wired through the same hooks-snippet.json) to an append-only JSONL file at .forge/journey/<run-id>.jsonl. Sensitive text is hashed (SHA-256, 16-char) and redacted before storage. Registered via forge sync — does not need to be invoked manually.
---

# journey-recorder — Copilot adapter

Registers the `journey_recorder` hook in a lab's `.github/hooks/hooks.json` so that every Copilot session activity is captured without any manual step.

## What it does

`forge sync` deep-merges `hooks-snippet.json` into the lab's `.github/hooks/hooks.json`. Once merged, Copilot fires `record-hook.sh` on the 4 supported lifecycle events, which builds a structured JSON event and pipes it to the shared `primitives/journey_recorder/shared/recorder.sh`. The recorder appends the event (with hash + preview for any `*_text` fields) to `.forge/journey/<run-id>.jsonl`.

## Copilot 4-event model vs. journey schema mapping

Copilot exposes 4 hook events. They map to the journey schema as follows:

| Copilot event    | Journey event type |
|---|---|
| `session-start`  | `session_start`    |
| `pre-request`    | `pre_tool_use`     |
| `post-response`  | `post_tool_use`    |
| `session-end`    | `session_end`      |

`UserPromptSubmit` has no direct Copilot analogue. The first `pre-request` in a session carries the initial user prompt context through the standard `$COPILOT_USER_INPUT` environment variable when available.

## Merge semantics

`forge sync` performs a **deep-merge** — it appends to existing hooks arrays rather than replacing them. Labs that already have `pre-request` hooks for other purposes are not affected. See `README.md` in the journey_recorder directory for details.

## Files shipped by forge sync

| Source (primitive library) | Destination (lab) |
|---|---|
| `adapters/copilot/hooks-snippet.json` | merged into `.github/hooks/hooks.json` |
| `adapters/copilot/record-hook.sh` | `.forge/primitives/journey_recorder/adapters/copilot/record-hook.sh` |
| `shared/recorder.sh` (via `primitives/journey_recorder/shared/recorder.sh`) | `.forge/primitives/journey_recorder/shared/recorder.sh` |

## Invariants

- Logic lives in `primitives/journey_recorder/shared/recorder.sh` in the Forge primitive library.
- DO NOT modify `record-hook.sh` or `hooks-snippet.json` directly in a lab — changes are overwritten on the next `forge sync`. Upstream changes flow through the library.
- The raw `*_text` payload is kept only in the local JSONL. Only `*_text_hash` and `*_text_preview` (80-char, secrets redacted) are forwarded to the telemetry pipeline.
