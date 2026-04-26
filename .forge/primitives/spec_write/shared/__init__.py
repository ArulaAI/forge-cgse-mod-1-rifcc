"""F5 /spec-write — shared package.

Exposes the top-level orchestrator:
  run(answers, output, dry_run, llm_backend) -> str
which chains: draft_spec → self_review → (optionally) write to disk.

For the full interview → draft → self-review → write pipeline, callers should
invoke run_interview() first to collect answers, then pass them to run().
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from primitives._llm import LLMBackend

from primitives.spec_write.shared.drafter import draft_spec
from primitives.spec_write.shared.interviewer import InterviewAnswer
from primitives.spec_write.shared.self_reviewer import SelfReviewIssue, self_review


def run(
    answers: Sequence[InterviewAnswer],
    output: Path,
    dry_run: bool,
    llm_backend: LLMBackend,
) -> str:
    """Orchestrate draft → self-review → (optional) write.

    Args:
        answers: Ordered InterviewAnswer list from run_interview().
        output: Target path for spec.md.
        dry_run: If True, return the spec text without writing to disk.
        llm_backend: LLM backend (MockBackend or BedrockBackend).

    Returns:
        The rendered spec.md as a string (regardless of dry_run).
    """
    spec_text = draft_spec(answers=answers, llm_backend=llm_backend)
    issues: list[SelfReviewIssue] = self_review(spec_text=spec_text, llm_backend=llm_backend)

    if issues:
        summary_lines = [f"  [{i.kind}] {i.location}: {i.description}" for i in issues]
        print(f"Self-review found {len(issues)} issue(s):\n" + "\n".join(summary_lines))
    else:
        print("Self-review passed — no issues found.")

    if not dry_run:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(spec_text)

    return spec_text


__all__ = [
    "InterviewAnswer",
    "SelfReviewIssue",
    "draft_spec",
    "run",
    "self_review",
]
