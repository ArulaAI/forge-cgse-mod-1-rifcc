"""Issue model, MarkdownIssueSource, and GitHubIssueSource (Task 9)."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Criterion:
    text: str
    done: bool = False


@dataclass
class Issue:
    id: str
    title: str
    domain: str
    priority: str = "standard"
    criteria: list[Criterion] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    body: str = ""


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


class IssueSource(Protocol):
    def fetch_issues(self, *, label: str | None = None) -> list[Issue]: ...

    def mark_issue_done(self, issue: Issue) -> None: ...


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^##\s+\[([^\]]+)\]\s+(.+)$")
_PRIORITY_RE = re.compile(r"^priority:\s*(\w+)\s*$", re.IGNORECASE)
_CHECKBOX_DONE_RE = re.compile(r"^-\s+\[x\]\s+(.+)$", re.IGNORECASE)
_CHECKBOX_TODO_RE = re.compile(r"^-\s+\[\s?\]\s+(.+)$")


# ---------------------------------------------------------------------------
# MarkdownIssueSource
# ---------------------------------------------------------------------------


def _parse_issues_from_text(text: str, *, skip_completed: bool = True) -> list[Issue]:
    """Parse issues from markdown text, returning Issue objects."""
    issues: list[Issue] = []
    current_domain: str | None = None
    current_title: str | None = None
    current_priority = "standard"
    current_criteria: list[Criterion] = []
    idx = 0

    def _flush() -> None:
        nonlocal idx
        if current_title is None:
            return
        if skip_completed and current_criteria and all(c.done for c in current_criteria):
            return
        issues.append(
            Issue(
                id=f"md-{idx}",
                title=current_title,
                domain=current_domain or "",
                priority=current_priority,
                criteria=list(current_criteria),
                labels=[current_domain] if current_domain else [],
            )
        )
        idx += 1

    for raw_line in text.splitlines():
        heading_match = _HEADING_RE.match(raw_line)
        if heading_match:
            _flush()
            current_domain = heading_match.group(1)
            current_title = heading_match.group(2).strip()
            current_priority = "standard"
            current_criteria = []
            continue

        priority_match = _PRIORITY_RE.match(raw_line)
        if priority_match:
            current_priority = priority_match.group(1).lower()
            continue

        done_match = _CHECKBOX_DONE_RE.match(raw_line)
        if done_match:
            current_criteria.append(Criterion(text=done_match.group(1).strip(), done=True))
            continue

        todo_match = _CHECKBOX_TODO_RE.match(raw_line)
        if todo_match:
            current_criteria.append(Criterion(text=todo_match.group(1).strip(), done=False))
            continue

    _flush()
    return issues


class MarkdownIssueSource:
    """Reads issues from a Markdown file."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def fetch_issues(self, *, label: str | None = None) -> list[Issue]:
        """Return open issues, optionally filtered by domain label."""
        if not self._path.exists():
            raise FileNotFoundError(f"Issue file not found: {self._path}")

        text = self._path.read_text(encoding="utf-8")
        issues = _parse_issues_from_text(text, skip_completed=True)

        if label is not None:
            issues = [i for i in issues if i.domain == label]

        # Sort: high priority first, preserve relative file order otherwise
        issues.sort(key=lambda i: 0 if i.priority == "high" else 1)
        return issues

    def mark_issue_done(self, issue: Issue) -> None:
        """Rewrite the file marking all unchecked criteria of *issue* as done."""
        if not self._path.exists():
            raise FileNotFoundError(f"Issue file not found: {self._path}")

        text = self._path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        result: list[str] = []

        in_target = False
        for raw_line in lines:
            heading_match = _HEADING_RE.match(raw_line.rstrip("\n"))
            if heading_match:
                domain = heading_match.group(1)
                title = heading_match.group(2).strip()
                in_target = domain == issue.domain and title == issue.title
                result.append(raw_line)
                continue

            if in_target:
                todo_match = _CHECKBOX_TODO_RE.match(raw_line.rstrip("\n"))
                if todo_match:
                    new_line = re.sub(r"^(- \[)\s?\]", r"\1x]", raw_line)
                    result.append(new_line)
                    continue

            result.append(raw_line)

        self._path.write_text("".join(result), encoding="utf-8")


# ---------------------------------------------------------------------------
# GitHubIssueSource
# ---------------------------------------------------------------------------


class GitHubIssueSource:
    """Fetches issues from GitHub via the ``gh`` CLI."""

    def __init__(
        self,
        priority_labels: list[str] | None = None,
        domain_order: list[str] | None = None,
    ) -> None:
        self._priority_labels = priority_labels or []
        self._domain_order = domain_order or []

    def fetch_issues(self, *, label: str | None = None) -> list[Issue]:
        """Fetch open GitHub issues, optionally filtered by label."""
        cmd = [
            "gh",
            "issue",
            "list",
            "--state",
            "open",
            "--json",
            "number,title,body,labels",
        ]
        if label:
            cmd += ["--label", label]

        proc = subprocess.run(  # noqa: S603
            cmd, capture_output=True, text=True, check=True
        )
        raw: list[dict[str, Any]] = json.loads(proc.stdout)

        issues: list[Issue] = []
        for item in raw:
            label_list = [lb["name"] for lb in item.get("labels", [])]
            domain = self._detect_domain(label_list)
            priority = self._detect_priority(label_list)
            criteria = self._parse_criteria(str(item.get("body") or ""))
            issues.append(
                Issue(
                    id=f"gh-{item['number']}",
                    title=str(item["title"]),
                    domain=domain,
                    priority=priority,
                    criteria=criteria,
                    labels=label_list,
                    body=str(item.get("body") or ""),
                )
            )

        issues.sort(key=self._sort_key)
        return issues

    def mark_issue_done(self, issue: Issue) -> None:
        """No-op: a PR with 'Closes #N' closes the issue automatically."""

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _detect_domain(self, labels: list[str]) -> str:
        for label in labels:
            if label in self._domain_order:
                return label
        return labels[0] if labels else ""

    def _detect_priority(self, labels: list[str]) -> str:
        for label in labels:
            if label in self._priority_labels:
                return "high"
        return "standard"

    @staticmethod
    def _parse_criteria(body: str) -> list[Criterion]:
        criteria: list[Criterion] = []
        for raw_line in body.splitlines():
            stripped = raw_line.strip()
            done_match = _CHECKBOX_DONE_RE.match(stripped)
            if done_match:
                criteria.append(Criterion(text=done_match.group(1).strip(), done=True))
                continue
            todo_match = _CHECKBOX_TODO_RE.match(stripped)
            if todo_match:
                criteria.append(Criterion(text=todo_match.group(1).strip(), done=False))
        return criteria

    def _sort_key(self, issue: Issue) -> tuple[int, int, int]:
        priority_rank = 0 if issue.priority == "high" else 1
        try:
            domain_rank = self._domain_order.index(issue.domain)
        except ValueError:
            domain_rank = len(self._domain_order)
        issue_num = int(issue.id.split("-", 1)[1]) if "-" in issue.id else 0
        return (priority_rank, domain_rank, issue_num)


# ---------------------------------------------------------------------------
# detect_source (Task 10)
# ---------------------------------------------------------------------------


def detect_source(*, explicit: str = "auto") -> str:
    """Return the issue source to use: ``"github"`` or ``"markdown"``.

    Args:
        explicit: One of ``"github"``, ``"markdown"``, or ``"auto"``.

    Returns:
        ``"github"`` or ``"markdown"``.
    """
    if explicit == "github":
        return "github"
    if explicit == "markdown":
        return "markdown"

    # Auto-detect: require both gh auth and a git remote
    try:
        gh_result = subprocess.run(
            ["gh", "auth", "status"],  # noqa: S607
            capture_output=True,
            check=False,
            timeout=10,
        )
        remote_result = subprocess.run(
            ["git", "remote", "-v"],  # noqa: S607
            capture_output=True,
            check=False,
            timeout=10,
        )
        if gh_result.returncode == 0 and remote_result.returncode == 0:
            return "github"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return "markdown"
