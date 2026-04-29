# U5 `/autowork` — Usage Examples

Five real-world patterns for invoking the autowork orchestrator in development,
lab exercises, and CI contexts. All examples assume the Forge primitive library
is on `PYTHONPATH` (or installed via `uv`) and the repo has a `.forge/autowork.yaml`.

---

## 1. Dry run against markdown issues

Preview what autowork would do before committing to a full execution. The dry run
prints the prioritized issue list with domain, stack, complexity, and criteria count
— no branches, commits, or PRs are created.

```bash
# From the repo root — preview all issues in .forge/issues.md
python -m primitives.autowork.shared.orchestrator . --dry-run --source markdown
```

Sample output:

```
AUTOWORK DRY RUN — Planned Execution Order:
  1. [primitives] #md-0 — Add token aggregator tests  stack=python+pydantic+yaml  model=planner  criteria=3
  2. [docs] #md-2 — Update README with autowork usage  stack=markdown  model=inline  criteria=2
  3. [infrastructure] #md-1 — Update CI pipeline  stack=shell+yaml  model=implementer  criteria=2
  4. [primitives] #md-3 — Fix domain router edge case  stack=python+pydantic+yaml  model=planner  criteria=2

Total: 4 issue(s) planned
```

Issues with `priority: high` are sorted ahead of standard-priority issues within
each priority tier, then by domain declaration order in `autowork.yaml`.

---

## 2. Dry run with label filter

Use `--label` to scope the dry run to a single domain. Useful when working on one
area of the codebase and you want to confirm only those issues appear before running.

```bash
# Preview only issues tagged [docs]
python -m primitives.autowork.shared.orchestrator . --dry-run --source markdown --label docs
```

Sample output:

```
AUTOWORK DRY RUN — Planned Execution Order:
  1. [docs] #md-2 — Update README with autowork usage  stack=markdown  model=inline  criteria=2

Total: 1 issue(s) planned
```

The `--label` flag matches the domain tag in `## [domain] Title` headings (markdown)
or issue label names (GitHub). Issues not matching the label are excluded entirely.

---

## 3. Full run against GitHub issues

Execute the autonomous loop against open GitHub issues. The orchestrator fetches
issues via the `gh` CLI, routes by label, implements criterion by criterion, and
creates + merges a PR for each. Requires `gh auth login` and a git remote.

```bash
# Full run — process all open issues labelled 'primitives'
python -m primitives.autowork.shared.orchestrator . --source github --label primitives
```

Expected flow for each issue:

```
[primitives] #42 — Add F2 spec-accuracy
  Branch: issue/42-add-f2-spec-accuracy
  Criterion 1/2: Implement spec-accuracy scorer ...
    → feat(primitives): implement spec-accuracy scorer  Refs: #42
  Criterion 2/2: Write unit tests for scorer ...
    → feat(primitives): add unit tests for spec-accuracy scorer  Refs: #42
  Final validate: uv run pytest -x && uv run ruff check .  ✓
  PR created: #43 — "feat(primitives): Add F2 spec-accuracy"
  Review: built-in (F3 not in manifest) — passed
  Merged (squash), branch deleted
  autowork_issue_complete: issue_id=42 status=merged pr_number=43

Session complete: 1 issue(s) processed, 0 skipped
Session report: .forge/autowork/autowork_2026-04-28T10-00-00Z.json
```

After all issues are exhausted the session report is written and the process exits 0.

---

## 4. Resume an interrupted session

If a previous run was interrupted (e.g. by a network error or Ctrl-C), use `--resume`
to pick up where it left off. The orchestrator scans for in-progress branches matching
`issue/*` or `autowork/*`, identifies remaining unchecked criteria, and continues.

```bash
# Resume the most recent interrupted session
python -m primitives.autowork.shared.orchestrator . --resume --source markdown
```

Resume logic:

1. Detects branch `autowork/md-1-update-ci-pipeline` still open
2. Reads `issue_id=md-1` from branch name
3. Finds criteria 2 still unchecked in `.forge/issues.md`
4. Resumes from criterion 2, continues normal loop
5. Exits 0 after processing all remaining issues

`--resume` can be combined with `--label` to resume only issues for a specific domain,
or with `--max-issues` to cap the session length.

---

## 5. Custom issues file

Use `--issues-file` when your issues live outside the default `.forge/issues.md` path —
for example in a sprint-scoped file or a shared multi-repo issues list.

```bash
# Run against a custom issues file in a sprint directory
python -m primitives.autowork.shared.orchestrator . \
  --dry-run \
  --source markdown \
  --issues-file .forge/sprints/sprint-4/issues.md
```

The `--issues-file` argument overrides `issue_source.markdown_path` in `autowork.yaml`
for the current invocation only — the config file is not modified.

Wiring the default path into `autowork.yaml` for a repo that keeps issues in a
non-standard location:

```yaml
issue_source:
  default: markdown
  markdown_path: .forge/sprints/current/issues.md
```

With this config, `--source markdown` (or auto-detected markdown mode) always reads
from the sprint file without needing `--issues-file` on every invocation.
