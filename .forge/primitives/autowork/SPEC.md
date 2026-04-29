# U5: /autowork — Forge primitive contract

## Purpose

Universal autonomous development loop that works through issues, routes each to the correct
domain, implements against acceptance criteria, validates, creates PRs, and optionally reviews
via F3 before merge. Operates without pausing or asking — the orchestrator is a state machine
that runs to completion.

## Layer

L2 Universal (U5) — every modernized lab/repo MUST ship this primitive (see Project 2 §4.2).

## Inputs

| Argument | Type | Default | Description |
|---|---|---|---|
| `lab_root` | path | `.` | Repo root |
| `--label` | string | none | Filter issues by label |
| `--max-issues` | int | unlimited | Cap issues per session |
| `--dry-run` | flag | false | Print plan without executing |
| `--resume` | flag | false | Resume an interrupted session |
| `--source` | `github\|markdown\|auto` | `auto` | Issue source |
| `--issues-file` | path | `.forge/issues.md` | Path to local issues markdown |

## Configuration: `.forge/autowork.yaml`

```yaml
# Issue source preferences
issue_source:
  default: auto                    # auto | github | markdown
  markdown_path: .forge/issues.md  # default path for markdown source
  priority_labels:                 # labels that boost issue priority (highest first)
    - critical-path
    - blocker
    - high-priority

# Domain matrix — keys match issue labels (GitHub) or [tags] (markdown)
domains:
  primitives:
    stack: "python+pydantic+yaml"
    validate: "uv run pytest -x && uv run ruff check . && uv run ruff format --check ."
    docs:
      - docs/primitive-authoring-guide.md
      - AGENTS.md
    complexity: high               # high | standard | mechanical

  infrastructure:
    stack: "shell+yaml"
    validate: "make verify"
    docs:
      - CONTRIBUTING.md
    complexity: standard

# Fallback domain — used when issue labels don't match any domain key
fallback_domain:
  stack: "python"
  validate: "uv run pytest -x"
  docs:
    - AGENTS.md
  complexity: standard

# Orchestration settings
orchestration:
  max_retries_per_criterion: 3
  max_review_cycles: 2
  commit_scope_from_domain: true
  branch_prefix:
    github: "issue"                # issue/<number>-<slug>
    markdown: "autowork"           # autowork/<slug>

# PR settings
pr:
  merge_method: squash             # squash | merge | rebase
  delete_branch_on_merge: true
  review_primitive: auto           # auto (use F3 if available) | f3 | builtin
```

Validated by Pydantic model (`AutoworkConfig`). `domains` must have at least one entry.
`complexity` must be `high`, `standard`, or `mechanical`. Missing optional sections get
defaults. Missing `autowork.yaml` entirely → exit 1.

## Logical model mapping

| Complexity | Logical name | Used for |
|---|---|---|
| `high` | `planner` | Issue parsing, novel implementation, architecture |
| `standard` | `implementer` | Well-patterned work, test writing |
| `mechanical` | `inline` | Lint fixes, commit messages |
| (always) | `reviewer` | PR review (when F3 unavailable) |

Logical model names are resolved by `primitives/_llm.py`'s llm-proxy. Names `planner`,
`implementer`, `inline`, and `reviewer` must be registered before U5 ships.

## Issue sources

### GitHub (`GitHubIssueSource`)

- Fetches via `gh issue list --state open --json number,title,body,labels`
- Filters by `--label` if provided
- Priority: priority labels → domain order (declaration order in `autowork.yaml`) → issue number
- Domain detection: matches issue labels against domain keys
- Branch: `issue/<number>-<slugified-title>`
- Completion: PR body includes `Closes #<number>`

### Markdown (`MarkdownIssueSource`)

- Parses `.forge/issues.md` (or `--issues-file` path)
- Format:
  ```markdown
  ## [domain] Issue title
  priority: high
  - [ ] Acceptance criterion 1
  - [ ] Acceptance criterion 2
  - [x] Already completed criterion
  ```
- `## [domain] Title` — H2 heading with domain tag in brackets
- `priority: <level>` — optional (high/standard, default: standard)
- `- [ ]` checkboxes are acceptance criteria; `- [x]` are skipped
- Issues with all criteria checked are skipped
- Completion: criteria checkboxes checked in-place (`- [ ]` → `- [x]`)

### Auto-detection

1. `--source github` explicitly → GitHub
2. `--source markdown` explicitly → Markdown
3. `gh auth status` succeeds + git remote exists → GitHub
4. Fallback → Markdown

## Orchestration loop

```
1. Load config from .forge/autowork.yaml
2. Initialize issue source (GitHub or Markdown)
3. Emit autowork_session_start journey event via U3
4. LOOP:
   a. Fetch next issue (filtered, prioritized)
   b. If none → print session report, emit autowork_session_end, exit 0
   c. Emit autowork_issue_start journey event
   d. Route to domain (match issue label/tag against domains config)
   e. Create branch
   f. Load domain docs (read files listed in domain.docs)
   g. Parse acceptance criteria (checkboxes)
   h. For each criterion:
      - Implement (model: domain complexity → logical name)
      - Write tests (model: implementer)
      - Validate (run domain.validate command)
      - If validation fails: fix, retry (max 3 per criterion)
      - If still failing: skip criterion, log blocker
      - Commit: feat(<domain>): <criterion summary>  Refs: #<issue>
   i. Final validation (full domain.validate)
   j. Push branch
   k. Create PR
   l. Review:
      - F3 available → delegate to F3 pr-review primitive
      - Else → built-in check (validation passed + tests green + lint clean)
      - Approved → merge (squash), delete branch
      - Changes requested → fix, re-push, re-review (max 2 cycles)
   m. Mark issue complete (GitHub: PR closes it; Markdown: check boxes)
   n. Emit autowork_issue_complete journey event
   o. Continue loop — NEVER pause or ask
5. Write session report → .forge/autowork/<session-id>.json
```

## Error handling

| Failure | Action |
|---|---|
| Criterion fails 3x | Skip criterion, log blocker, continue to next criterion |
| Branch/push/PR creation fails | Skip issue, log, continue to next issue |
| Review fails after 2 fix cycles | Leave PR open with warning, continue to next issue |
| Missing `autowork.yaml` | Exit 1 immediately |
| Malformed `autowork.yaml` | Exit 1 with validation error showing which field(s) failed |

## Resume (`--resume`)

1. Scan for in-progress branches matching `issue/*` or `autowork/*`
2. Identify corresponding issue from branch name
3. Determine remaining unchecked criteria
4. Resume from last committed criterion
5. Continue main loop after current issue

## Dry run (`--dry-run`)

Prints ordered list of issues with domain routing, complexity, validation commands, and
criteria count. No branches, commits, or PRs are created. Exit 0.

## Outputs

- Merged PRs — one per completed issue
- `.forge/autowork/<session-id>.json` — structured session report (see design spec §4 for schema)
- Journey events via U3 — `autowork_session_start`, `autowork_issue_start`,
  `autowork_criterion_complete`, `autowork_criterion_skipped`, `autowork_issue_complete`,
  `autowork_session_end`

## Exit codes

| Code | Meaning |
|---|---|
| `0` | All issues processed (some may have been skipped) |
| `1` | Fatal config error (missing or malformed `autowork.yaml`) |

## F3 integration

If `f3` or `pr_review` is listed in `.forge/manifest.yaml` primitives, delegate PR review to
F3 `/pr-review`. Otherwise run built-in validation-only check: domain `validate` command
passes + lint clean. Graceful degradation — U5 never requires F3 to complete.

## Implementation model

`shared/orchestrator.py` is a state machine and workflow controller, not a code generator.
It manages config loading, issue selection, domain routing, session reporting, journey event
emission, and the PR lifecycle (branch, push, create, merge). Criterion implementation —
reading code, writing code, running tests — is delegated to the harness's native AI
capabilities via the adapter layer. The orchestrator invokes the harness agent with structured
context: the criterion text, domain stack, loaded docs, and the resolved logical model name.

## Adapters

- Claude Code: `adapters/claude_code/SKILL.md` + `invoke.sh`
- Copilot: `adapters/copilot/SKILL.md` + `github-bundle/skills/autowork/SKILL.md`
  + `github-bundle/prompts/autowork.prompt.md`

## Related primitives

| Primitive | Relationship |
|---|---|
| U3 `/journey-recorder` | U5 emits journey events through U3 |
| U2 `/lab-grader` | Can consume autowork journey events as rubric evidence |
| F3 `/pr-review` | Optional deep PR review (graceful degradation if absent) |
