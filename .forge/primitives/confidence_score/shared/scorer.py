"""F1 confidence scorer — rubric-driven, LLM-judged.

Loads ``rubric.yaml`` (co-located), builds a structured prompt asking the LLM
to score each dimension 0.0-1.0, parses the JSON response, and returns a
``ScoreResult``.  Raises ``GateBlockedError`` when a threshold is set and the
weighted score falls below it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel

from primitives._llm import BedrockBackend, LLMBackend, MockBackend

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

ConfidenceLevel = Literal["low", "medium", "high"]


class DimensionResult(BaseModel):
    """Per-dimension score returned by the LLM."""

    id: str
    score: float
    reasoning: str


class ScoreResult(BaseModel):
    """Aggregate result produced by ``score_artifact``."""

    level: ConfidenceLevel
    weighted_score: float
    dimensions: list[DimensionResult]
    gate_passed: bool


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class GateBlockedError(RuntimeError):
    """Raised when the gate flag is set and the score falls below the threshold.

    Attributes:
        level: The ``ConfidenceLevel`` that triggered the block.
    """

    def __init__(self, level: ConfidenceLevel, threshold: str, weighted_score: float) -> None:
        super().__init__(
            f"Confidence gate blocked: level={level!r} is below threshold={threshold!r} "
            f"(weighted_score={weighted_score:.4f})"
        )
        self.level: ConfidenceLevel = level
        self.threshold = threshold
        self.weighted_score = weighted_score


# ---------------------------------------------------------------------------
# Rubric loading
# ---------------------------------------------------------------------------

_RUBRIC_PATH = Path(__file__).parent / "rubric.yaml"


def _load_rubric() -> dict[str, Any]:
    """Read and return rubric.yaml relative to this file."""
    with _RUBRIC_PATH.open() as fh:
        data: dict[str, Any] = yaml.safe_load(fh)
        return data


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------


def _build_system_prompt(dimensions: list[dict[str, Any]]) -> str:
    dim_lines = "\n".join(
        f"  - {d['id']}: {d['description']} (weight {d['weight']})" for d in dimensions
    )
    return (
        "You are a code and artifact quality evaluator.\n"
        "Score the provided artifact on each of the following dimensions from 0.0 (lowest) "
        "to 1.0 (highest):\n"
        f"{dim_lines}\n\n"
        "Return ONLY valid JSON in exactly this shape — no markdown fences, no prose:\n"
        '{"dimensions": {'
        '"<dimension_id>": {"score": <float 0-1>, "reasoning": "<one sentence>"}, ...'
        "}}"
    )


def _build_user_prompt(artifact_text: str, context: str | None) -> str:
    parts: list[str] = []
    if context:
        parts.append(f"Additional context provided by the caller:\n{context}\n")
    parts.append("Artifact to evaluate:\n```\n" + artifact_text + "\n```")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Level resolution
# ---------------------------------------------------------------------------


def _resolve_level(weighted_score: float, thresholds: dict[str, Any]) -> ConfidenceLevel:
    """Map a weighted score to a ConfidenceLevel using rubric thresholds."""
    high_cfg = thresholds.get("high", {})
    medium_cfg = thresholds.get("medium", {})
    if isinstance(high_cfg, dict):
        min_high = high_cfg.get("min_weighted_score", 0.70)
        if weighted_score >= float(min_high):
            return "high"
    if isinstance(medium_cfg, dict):
        min_med = medium_cfg.get("min_weighted_score", 0.40)
        if weighted_score >= float(min_med):
            return "medium"
    return "low"


def _threshold_order(level: ConfidenceLevel) -> int:
    return {"low": 0, "medium": 1, "high": 2}[level]


# ---------------------------------------------------------------------------
# Core scoring function
# ---------------------------------------------------------------------------


def score_artifact(
    target_path: str | Path,
    *,
    context: str | None,
    llm_backend: LLMBackend,
    threshold: str | None = None,
) -> ScoreResult:
    """Score an artifact file via LLM-judged rubric evaluation.

    Args:
        target_path: Path to the file to evaluate.
        context: Optional free-text context supplied by the caller (e.g. environment notes).
        llm_backend: An ``LLMBackend`` instance (``MockBackend`` or ``BedrockBackend``).
        threshold: Optional gate level — ``'low'``, ``'medium'``, or ``'high'``.
                   When set and the resulting level is below this threshold,
                   ``GateBlockedError`` is raised.

    Returns:
        A ``ScoreResult`` describing the level, weighted score, and per-dimension results.

    Raises:
        GateBlockedError: When ``threshold`` is set and the score falls below it.
        FileNotFoundError: When ``target_path`` does not exist.
    """
    rubric = _load_rubric()
    dimensions: list[dict[str, Any]] = rubric["dimensions"]
    thresholds: dict[str, Any] = rubric["thresholds"]

    artifact_text = Path(target_path).read_text(encoding="utf-8")

    system = _build_system_prompt(dimensions)
    user = _build_user_prompt(artifact_text, context)

    raw = llm_backend.complete(system=system, user=user, model_logical="grader")

    # --- Parse LLM response ---------------------------------------------------
    try:
        parsed = json.loads(raw)
        dims_raw: dict[str, dict[str, Any]] = parsed["dimensions"]
        dim_results: list[DimensionResult] = []
        for d in dimensions:
            dim_id = str(d["id"])
            dim_data = dims_raw.get(dim_id, {"score": 0.0, "reasoning": "missing"})
            dim_results.append(
                DimensionResult(
                    id=dim_id,
                    score=float(dim_data.get("score", 0.0)),
                    reasoning=str(dim_data.get("reasoning", "")),
                )
            )
        # Compute weighted score
        weighted = sum(
            dr.score * float(d["weight"]) for dr, d in zip(dim_results, dimensions, strict=True)
        )
        level = _resolve_level(weighted, thresholds)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        # Malformed response — return a low-confidence fallback, no gate raise
        dim_results = [
            DimensionResult(id=str(d["id"]), score=0.0, reasoning="LLM response parse error")
            for d in dimensions
        ]
        weighted = 0.0
        level = "low"
        return ScoreResult(
            level=level,
            weighted_score=weighted,
            dimensions=dim_results,
            gate_passed=False,
        )

    # Determine gate status
    gate_passed: bool
    if threshold is not None:
        threshold_norm: ConfidenceLevel = threshold.lower()  # type: ignore[assignment]
        gate_passed = _threshold_order(level) >= _threshold_order(threshold_norm)
    else:
        gate_default: ConfidenceLevel = str(rubric.get("gate_default", "medium"))  # type: ignore[assignment]
        gate_passed = _threshold_order(level) >= _threshold_order(gate_default)

    result = ScoreResult(
        level=level,
        weighted_score=weighted,
        dimensions=dim_results,
        gate_passed=gate_passed,
    )

    if threshold is not None and not gate_passed:
        raise GateBlockedError(
            level=level,
            threshold=threshold,
            weighted_score=weighted,
        )

    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    """Argparse CLI wrapping ``score_artifact``."""
    parser = argparse.ArgumentParser(
        prog="scorer",
        description="F1 confidence scorer — rate an artifact Low/Medium/High",
    )
    parser.add_argument("target", help="Path to the artifact file to score")
    parser.add_argument("--context", default=None, help="Optional free-text context")
    parser.add_argument(
        "--threshold",
        choices=["low", "medium", "high"],
        default=None,
        help="Gate threshold; exit 1 if score is below this level",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--backend",
        choices=["bedrock", "mock"],
        default="bedrock",
        help="LLM backend to use (default: bedrock)",
    )
    args = parser.parse_args(argv)

    backend = MockBackend() if args.backend == "mock" else BedrockBackend()

    try:
        result = score_artifact(
            args.target,
            context=args.context,
            llm_backend=backend,
            threshold=args.threshold,
        )
    except GateBlockedError as exc:
        if args.format == "json":
            print(json.dumps({"level": exc.level, "gate_passed": False, "error": str(exc)}))
        else:
            print(f"GATE BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "level": result.level,
                    "weighted_score": result.weighted_score,
                    "gate_passed": result.gate_passed,
                    "dimensions": [d.model_dump() for d in result.dimensions],
                },
                indent=2,
            )
        )
    else:
        print(f"Confidence level : {result.level.upper()}")
        print(f"Weighted score   : {result.weighted_score:.4f}")
        print(f"Gate passed      : {result.gate_passed}")
        print()
        for d in result.dimensions:
            print(f"  [{d.id}] {d.score:.2f} — {d.reasoning}")


if __name__ == "__main__":
    main()
