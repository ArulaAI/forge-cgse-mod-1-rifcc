"""Autowork orchestrator state machine and CLI entry point (Task 16)."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from primitives.autowork.shared.config import AutoworkConfig, ConfigError, load_config
from primitives.autowork.shared.domain_router import route_issue
from primitives.autowork.shared.issue_sources import (
    GitHubIssueSource,
    IssueSource,
    MarkdownIssueSource,
    detect_source,
)
from primitives.autowork.shared.session_report import (  # noqa: F401
    CompletedIssue,
    SessionReport,
    SkippedIssue,
    print_summary,
    write_report,
)

__all__ = [
    "dry_run",
    "generate_branch_name",
    "generate_session_id",
    "main",
]


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def generate_session_id() -> str:
    """Return a unique session identifier stamped with the current UTC time.

    Returns:
        A string of the form ``autowork_YYYY-MM-DDTHH-MM-SSZ``.
    """
    now = datetime.now(UTC)
    return f"autowork_{now.strftime('%Y-%m-%dT%H-%M-%SZ')}"


def generate_branch_name(*, issue_id: str, title: str, prefix: str) -> str:
    """Generate a Git branch name from an issue id, title, and prefix.

    Args:
        issue_id: The issue identifier (e.g. ``"42"`` or ``"md-0"``).
        title: The human-readable issue title.
        prefix: The branch namespace prefix (e.g. ``"issue"`` or ``"autowork"``).

    Returns:
        A branch name of the form ``{prefix}/{issue_id}-{slug}`` where slug is
        a lower-cased, hyphenated version of *title* truncated to 50 characters.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = slug[:50]
    return f"{prefix}/{issue_id}-{slug}"


# ---------------------------------------------------------------------------
# Dry-run planner
# ---------------------------------------------------------------------------


def dry_run(
    *,
    config: AutoworkConfig,
    source: IssueSource,
    label: str | None = None,
) -> None:
    """Print a planned execution order without making any changes.

    Args:
        config: The parsed autowork configuration.
        source: The issue source to fetch issues from.
        label: Optional domain label to filter issues.
    """
    issues = source.fetch_issues(label=label)

    print("AUTOWORK DRY RUN — Planned Execution Order:")

    if not issues:
        print("No issues found")
        return

    for idx, issue in enumerate(issues, start=1):
        routed = route_issue(issue, config)
        criteria_count = len(issue.criteria)
        print(
            f"  {idx}. [{routed.domain_key}] #{issue.id} — {issue.title}"
            f"  stack={routed.domain_config.stack}"
            f"  model={routed.logical_model}"
            f"  criteria={criteria_count}"
        )

    print(f"\nTotal: {len(issues)} issue(s) planned")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    """Autowork CLI entry point.

    Args:
        argv: Argument list (defaults to :data:`sys.argv[1:]`).
    """
    parser = argparse.ArgumentParser(
        prog="autowork",
        description="Autowork orchestrator — autonomously resolves lab issues.",
    )
    parser.add_argument(
        "lab_root",
        nargs="?",
        default=".",
        help="Root directory of the lab workspace (default: current directory).",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="Filter issues by domain label.",
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=None,
        help="Maximum number of issues to process.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned execution order without making changes.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume a previous session.",
    )
    parser.add_argument(
        "--source",
        choices=["github", "markdown", "auto"],
        default="auto",
        help="Issue source (default: auto).",
    )
    parser.add_argument(
        "--issues-file",
        default=None,
        help="Path to the markdown issues file (overrides config).",
    )

    args = parser.parse_args(argv)
    lab_root = Path(args.lab_root)
    config_path = lab_root / ".forge" / "autowork.yaml"

    try:
        config = load_config(config_path)
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Resolve the issue source
    source_type = detect_source(explicit=args.source)

    if source_type == "github":
        issue_source: IssueSource = GitHubIssueSource(
            priority_labels=config.issue_source.priority_labels,
        )
    else:
        markdown_path = (
            Path(args.issues_file)
            if args.issues_file
            else lab_root / config.issue_source.markdown_path
        )
        issue_source = MarkdownIssueSource(markdown_path)

    if args.dry_run:
        dry_run(config=config, source=issue_source, label=args.label)
        return

    print(
        "Full execution requires harness integration. Use --dry-run to preview the execution plan.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
