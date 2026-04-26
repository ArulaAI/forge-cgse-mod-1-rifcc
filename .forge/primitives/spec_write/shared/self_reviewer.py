"""F5 /spec-write — static + LLM self-reviewer.

Two-phase approach:
  1. _static_checks(spec_text): regex-based — finds <!-- placeholder --> patterns,
     checks all 6 headings are present, checks no section is empty (< 10 chars after
     the heading before the next heading or EOF).
  2. LLM call: asks the model to find contradictions, ambiguities, and scope creep.
     Parses JSON response. Malformed JSON → no LLM issues (static issues still apply).

Returns list[SelfReviewIssue].
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

if TYPE_CHECKING:
    from primitives._llm import LLMBackend

SelfReviewIssueKind = Literal[
    "placeholder", "contradiction", "ambiguity", "missing_section", "scope_creep"
]

_REQUIRED_HEADINGS = [
    "## Goal",
    "## Architecture",
    "## File structure",
    "## Acceptance criteria",
    "## Risks",
    "## Decision log",
]

_PLACEHOLDER_PATTERN = re.compile(r"<!--\s*placeholder\s*-->", re.IGNORECASE)

_LLM_SYSTEM = """\
You are a spec quality reviewer. Analyse the spec.md below and find any of:
- contradictions between sections (e.g. goal says X but constraints say ¬X)
- ambiguities (vague terms with no measurable definition)
- scope creep (new requirements not mentioned in Goal)

Respond with a JSON object ONLY — no prose, no code fences:
{"issues": [{"kind": "contradiction|ambiguity|scope_creep",
             "description": "...", "location": "..."}]}

If there are no issues, respond with: {"issues": []}
"""


class SelfReviewIssue(BaseModel):
    """A single finding from the self-review pass."""

    kind: SelfReviewIssueKind
    description: str
    location: str


def _static_checks(spec_text: str) -> list[SelfReviewIssue]:
    """Run deterministic, regex-based checks — no LLM required."""
    issues: list[SelfReviewIssue] = []

    # 1. Placeholder detection
    for match in _PLACEHOLDER_PATTERN.finditer(spec_text):
        # Find approximate location (heading above the match)
        preceding = spec_text[: match.start()]
        heading_matches = list(re.finditer(r"^##+ .+", preceding, re.MULTILINE))
        location = heading_matches[-1].group() if heading_matches else "preamble"
        issues.append(
            SelfReviewIssue(
                kind="placeholder",
                description="Found an unfilled placeholder comment.",
                location=location,
            )
        )

    # 2. Missing section headings
    for heading in _REQUIRED_HEADINGS:
        if heading not in spec_text:
            issues.append(
                SelfReviewIssue(
                    kind="missing_section",
                    description=f"Required section '{heading}' is absent.",
                    location="document",
                )
            )

    # 3. Empty sections — fewer than this many chars after heading = effectively empty
    _MIN_SECTION_CHARS = 10
    heading_pattern = re.compile(r"^##+ .+", re.MULTILINE)
    heading_positions = [(m.start(), m.group()) for m in heading_pattern.finditer(spec_text)]
    for i, (pos, heading) in enumerate(heading_positions):
        end = heading_positions[i + 1][0] if i + 1 < len(heading_positions) else len(spec_text)
        section_body = spec_text[pos + len(heading) : end].strip()
        if len(section_body) < _MIN_SECTION_CHARS:
            issues.append(
                SelfReviewIssue(
                    kind="ambiguity",
                    description=f"Section '{heading}' appears empty or nearly empty.",
                    location=heading,
                )
            )

    return issues


def self_review(
    spec_text: str,
    llm_backend: LLMBackend,
) -> list[SelfReviewIssue]:
    """Review the spec for quality issues.

    Runs static checks first (always), then calls the LLM for semantic checks.
    Malformed LLM JSON is silently ignored — static issues are always returned.

    Args:
        spec_text: Full Markdown content of the spec to review.
        llm_backend: LLM backend (MockBackend or BedrockBackend).

    Returns:
        Combined list of SelfReviewIssue from both passes.
    """
    issues: list[SelfReviewIssue] = _static_checks(spec_text)

    # LLM pass — parse JSON; fall back gracefully on malformed response
    try:
        raw = llm_backend.complete(
            system=_LLM_SYSTEM,
            user=spec_text,
            model_logical="default",
        )
        data = json.loads(raw)
        for item in data.get("issues", []):
            try:
                issues.append(
                    SelfReviewIssue(
                        kind=item["kind"],
                        description=item.get("description", ""),
                        location=item.get("location", ""),
                    )
                )
            except (KeyError, ValueError):
                pass  # skip malformed individual items
    except (json.JSONDecodeError, KeyError, TypeError):
        pass  # malformed JSON → only static issues returned

    return issues
