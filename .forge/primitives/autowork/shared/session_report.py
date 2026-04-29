"""Session report writer and summary printer for autowork (Task 14)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class CompletedIssue:
    """A successfully completed issue."""

    id: str
    title: str
    domain: str
    pr: int | None = None
    status: str = "merged"


@dataclass
class SkippedIssue:
    """An issue that was skipped during the session."""

    id: str
    title: str
    domain: str
    reason: str = ""
    blocker: str = ""


@dataclass
class SessionReport:
    """Aggregate report for a single autowork session."""

    session_id: str
    source: str
    started_at: str = ""
    ended_at: str = ""
    total_commits: int = 0
    completed: list[CompletedIssue] = field(default_factory=list)
    skipped: list[SkippedIssue] = field(default_factory=list)
    token_usage: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def issues_total(self) -> int:
        """Total number of issues attempted (completed + skipped)."""
        return len(self.completed) + len(self.skipped)

    @property
    def issues_completed(self) -> int:
        """Number of successfully completed issues."""
        return len(self.completed)

    @property
    def issues_skipped(self) -> int:
        """Number of skipped issues."""
        return len(self.skipped)

    @property
    def prs_created(self) -> int:
        """Number of pull requests created (completed issues with a PR number)."""
        return sum(1 for c in self.completed if c.pr is not None)

    @property
    def prs_merged(self) -> int:
        """Number of pull requests merged (completed issues with status='merged')."""
        return sum(1 for c in self.completed if c.pr is not None and c.status == "merged")

    @property
    def duration_seconds(self) -> float | None:
        """Session duration in seconds, or None if timestamps are unavailable."""
        if not self.started_at or not self.ended_at:
            return None
        try:
            start = datetime.fromisoformat(self.started_at.rstrip("Z")).replace(tzinfo=UTC)
            end = datetime.fromisoformat(self.ended_at.rstrip("Z")).replace(tzinfo=UTC)
            return (end - start).total_seconds()
        except ValueError:
            return None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialise the report to a plain dictionary."""
        return {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_seconds": self.duration_seconds,
            "source": self.source,
            "issues_total": self.issues_total,
            "issues_completed": self.issues_completed,
            "issues_skipped": self.issues_skipped,
            "prs_created": self.prs_created,
            "prs_merged": self.prs_merged,
            "total_commits": self.total_commits,
            "completed": [
                {
                    "id": c.id,
                    "title": c.title,
                    "domain": c.domain,
                    "pr": c.pr,
                    "status": c.status,
                }
                for c in self.completed
            ],
            "skipped": [
                {
                    "id": s.id,
                    "title": s.title,
                    "domain": s.domain,
                    "reason": s.reason,
                    "blocker": s.blocker,
                }
                for s in self.skipped
            ],
        }


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def write_report(*, lab_root: Path, report: SessionReport) -> Path:
    """Write *report* as JSON to ``.forge/autowork/<session-id>.json``.

    Args:
        lab_root: Root directory of the lab workspace.
        report: The session report to persist.

    Returns:
        The path of the written file.
    """
    out_dir = lab_root / ".forge" / "autowork"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{report.session_id}.json"
    out_path.write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return out_path


def print_summary(report: SessionReport) -> None:
    """Print a human-readable summary of *report* to stdout.

    Args:
        report: The session report to summarise.
    """
    print(f"Session: {report.session_id}  source={report.source}")
    if report.started_at:
        print(f"  Started:  {report.started_at}")
    if report.ended_at:
        print(f"  Ended:    {report.ended_at}")
    dur = report.duration_seconds
    if dur is not None:
        print(f"  Duration: {dur:.0f}s")
    print(
        f"  Issues:   {report.issues_total} total, "
        f"{report.issues_completed} completed, "
        f"{report.issues_skipped} skipped"
    )
    print(f"  PRs:      {report.prs_created} created, {report.prs_merged} merged")
    print(f"  Commits:  {report.total_commits}")
    if report.completed:
        print("  Completed:")
        for c in report.completed:
            pr_str = f" (PR #{c.pr})" if c.pr is not None else ""
            print(f"    - [{c.domain}] {c.title}{pr_str}")
    if report.skipped:
        print("  Skipped:")
        for s in report.skipped:
            reason_str = f" — {s.reason}" if s.reason else ""
            print(f"    - [{s.domain}] {s.title}{reason_str}")
