# Contributing

## Pre-flight (first time)

```bash
# Install Python dependencies
uv sync

# Install pre-commit hooks (ruff, shellcheck, forge validate --naming-only)
lefthook install

# Sync Forge primitives from the pinned version in .forge/manifest.yaml
forge sync
# or: make sync
```

## Day-to-day workflow

```bash
# Run tests
make test
# or: uv run pytest tests/

# Validate lab structure and naming
make validate
# or: forge validate .

# Grade your work (runs the L2 lab grader)
make grade
```

## Commit conventions

Follow Project 2 conventions (matches `arula-ai/forge-prowess-labs-modernization`):

| Prefix | When to use |
|---|---|
| `chore(<scope>):` | Scaffolding, dependency bumps, tooling config |
| `feat(<scope>):` | New exercises, new L3 primitives, new skills |
| `fix(<scope>):` | Bug fixes in starter code, grader criteria, adapter scripts |
| `docs(<scope>):` | Docs, overview, facilitator guide, grading rubric |
| `test(<scope>):` | New or updated tests |
| `refactor(<scope>):` | Internal restructuring without behaviour change |

Include a `Closes #<issue>` reference in the commit body when resolving a tracker issue.

## CI note

> **CI is dormant until GitHub Actions budget refreshes (ADR 0004).** The `.github/workflows/validate.yml` workflow is `on: workflow_dispatch:` only. Run `make validate` and `make test` locally before opening a PR.

## Authoring an L3 primitive

L3 primitives live in `.forge/local/primitives/`. Each is a directory with:

```text
.forge/local/primitives/<name>/
  README.md          # What the primitive does and how to use it
  shared/            # Core implementation (language-agnostic where possible)
  adapters/
    claude_code/     # Claude Code adapter (SKILL.md + record.sh if needed)
    copilot/         # Copilot adapter (github-bundle/ with .md files)
  tests/             # Unit tests for the primitive logic
```

Steps:

1. Create the directory structure above.
2. Implement `shared/` logic.
3. Write adapter files for both Claude Code and Copilot.
4. Add tests under `tests/`.
5. Run `forge validate .` — it should pass without warnings.
6. Reference the primitive from `.forge/grader.yaml` if grading behavior depends on it.

## Pull request checklist

- [ ] `make validate` exits 0
- [ ] `make test` exits 0
- [ ] `lefthook` pre-commit hooks pass (auto-run on `git commit`)
- [ ] All `<placeholder>` tokens removed from committed files
- [ ] Journey recorder hooks are still active in `.claude/settings.json`
- [ ] PR body references the tracker issue (`Closes #N`)
