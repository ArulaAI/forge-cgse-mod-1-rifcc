"""F4 /hypothesis validator — LLM-judged evidence evaluation.

Reads an existing ``hypothesis.md``, combines it with caller-supplied
evidence text, and asks the LLM to classify support as
``supported`` / ``inconclusive`` / ``refuted`` with reasoning.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from primitives._llm import BedrockBackend, LLMBackend, MockBackend

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

SupportLevel = Literal["supported", "inconclusive", "refuted"]


class ValidationResult(BaseModel):
    """Result of a hypothesis validation call."""

    support_level: SupportLevel
    reasoning: str
    evidence_refs: list[str]


# ---------------------------------------------------------------------------
# Core validate function
# ---------------------------------------------------------------------------

_SYSTEM = (
    "You are an expert engineering coach evaluating whether observed evidence supports "
    "a software engineering hypothesis.\n\n"
    "Classify the hypothesis support level as exactly one of: supported, inconclusive, refuted.\n\n"
    "- supported: the evidence clearly confirms the hypothesis.\n"
    "- inconclusive: the evidence is consistent with the hypothesis but does not confirm it.\n"
    "- refuted: the evidence contradicts the hypothesis.\n\n"
    "Return ONLY valid JSON in exactly this shape — no markdown fences, no prose:\n"
    '{"support_level": "<supported|inconclusive|refuted>", '
    '"reasoning": "<2-4 sentences>", '
    '"evidence_refs": ["<file:line or description>", ...]}'
)


def validate(
    hypothesis_file: Path,
    evidence_text: str,
    llm_backend: LLMBackend,
) -> ValidationResult:
    """Evaluate whether evidence supports the hypothesis in ``hypothesis_file``.

    Args:
        hypothesis_file: Path to ``hypothesis.md`` (must exist).
        evidence_text: Free-text description of evidence gathered (test results,
            code changes, profiler output, etc.).
        llm_backend: An ``LLMBackend`` instance (``MockBackend`` or ``BedrockBackend``).

    Returns:
        A ``ValidationResult`` with ``support_level``, ``reasoning``, and ``evidence_refs``.

    Raises:
        FileNotFoundError: When ``hypothesis_file`` does not exist.
    """
    hypothesis_file = Path(hypothesis_file)
    if not hypothesis_file.exists():
        raise FileNotFoundError(f"hypothesis.md not found: {hypothesis_file}")

    hypothesis_text = hypothesis_file.read_text(encoding="utf-8")

    user = f"## Hypothesis document\n\n{hypothesis_text}\n\n## Evidence\n\n{evidence_text}"

    raw = llm_backend.complete(system=_SYSTEM, user=user, model_logical="grader")

    # --- Parse LLM response ---------------------------------------------------
    try:
        parsed = json.loads(raw)
        support_raw = str(parsed.get("support_level", "inconclusive")).lower()
        if support_raw not in ("supported", "inconclusive", "refuted"):
            support_raw = "inconclusive"
        return ValidationResult(
            support_level=support_raw,  # type: ignore[arg-type]
            reasoning=str(parsed.get("reasoning", "No reasoning provided.")),
            evidence_refs=[str(r) for r in parsed.get("evidence_refs", [])],
        )
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return ValidationResult(
            support_level="inconclusive",
            reasoning="LLM response could not be parsed; defaulting to inconclusive.",
            evidence_refs=[],
        )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    """Argparse CLI for the hypothesis validator."""
    parser = argparse.ArgumentParser(
        prog="validator",
        description="F4 /hypothesis --validate: evaluate evidence against hypothesis.md",
    )
    parser.add_argument(
        "hypothesis_file",
        nargs="?",
        default="hypothesis.md",
        help="Path to hypothesis.md (default: ./hypothesis.md)",
    )
    parser.add_argument(
        "--evidence",
        default="",
        help="Evidence text to evaluate against the hypothesis",
    )
    parser.add_argument(
        "--backend",
        choices=["bedrock", "mock"],
        default="bedrock",
        help="LLM backend to use (default: bedrock)",
    )
    args = parser.parse_args(argv)

    backend: LLMBackend = MockBackend() if args.backend == "mock" else BedrockBackend()
    result = validate(
        hypothesis_file=Path(args.hypothesis_file),
        evidence_text=args.evidence,
        llm_backend=backend,
    )
    print(f"Support level : {result.support_level.upper()}")
    print(f"Reasoning     : {result.reasoning}")
    if result.evidence_refs:
        print(f"Evidence refs : {', '.join(result.evidence_refs)}")


if __name__ == "__main__":
    main()
