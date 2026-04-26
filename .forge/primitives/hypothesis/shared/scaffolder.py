"""F4 /hypothesis scaffolder — interactive 5-question hypothesis builder.

Loads ``questions.yaml`` (co-located), iterates the 5 questions, calls the LLM
once per question to elaborate the user's answer, assembles a structured
``hypothesis.md``, and writes it to ``{target_dir}/hypothesis.md``.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from primitives._llm import BedrockBackend, LLMBackend, MockBackend

# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------

_QUESTIONS_PATH = Path(__file__).parent / "questions.yaml"


def _load_questions() -> list[dict[str, Any]]:
    """Return the list of question dicts from questions.yaml."""
    with _QUESTIONS_PATH.open() as fh:
        data: dict[str, Any] = yaml.safe_load(fh)
        return list(data["questions"])


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

_HEADING_MAP = {
    "q1_observation": "## Hypothesis",
    "q2_mechanism": "## Mechanism",
    "q3_prediction": "## Predictions",
    "q4_null": "## Null Condition",
    "q5_confidence": "## Confidence",
}


def _render_hypothesis(elaborations: list[tuple[str, str]]) -> str:
    """Render the hypothesis.md content from (question_id, elaboration) pairs.

    Args:
        elaborations: A list of (question_id, elaborated_text) tuples in order.

    Returns:
        The full Markdown string for hypothesis.md.
    """
    lines: list[str] = []
    for q_id, text in elaborations:
        heading = _HEADING_MAP.get(q_id, f"## {q_id}")
        lines.append(heading)
        lines.append("")
        lines.append(text.strip())
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core scaffold function
# ---------------------------------------------------------------------------


def scaffold(
    target_dir: Path,
    llm_backend: LLMBackend,
    answers_override: list[str] | None = None,
) -> Path:
    """Scaffold a hypothesis.md by iterating the 5 questions with LLM elaboration.

    Args:
        target_dir: Directory where ``hypothesis.md`` will be written.
        llm_backend: An ``LLMBackend`` instance (``MockBackend`` or ``BedrockBackend``).
        answers_override: Optional list of 5 pre-supplied user answers (used in tests
            to avoid interactive prompts). If ``None``, each answer is solicited
            from stdin via ``input()``.

    Returns:
        The ``Path`` to the written ``hypothesis.md``.
    """
    questions = _load_questions()
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    elaborations: list[tuple[str, str]] = []
    accumulated_context = ""

    for i, question in enumerate(questions):
        q_id: str = question["id"]
        q_prompt: str = question["prompt"]
        q_purpose: str = question.get("purpose", "")

        # Obtain user answer
        if answers_override is not None:
            user_answer = answers_override[i] if i < len(answers_override) else ""
        else:
            print(f"\nQ{i + 1}: {q_prompt}")
            user_answer = input("> ").strip()

        # Build system prompt containing the question
        system = (
            f"You are an expert engineering coach helping a developer articulate a hypothesis.\n"
            f"The developer is answering this question:\n\n"
            f"  {q_prompt}\n\n"
            f"Purpose: {q_purpose}\n\n"
            f"Elaborate the developer's answer into a clear, concise, technically precise "
            f"paragraph suitable for a hypothesis document. Preserve all technical claims. "
            f"Do not add information not implied by the answer. Return plain text only."
        )

        # User prompt: the answer + accumulated context from prior questions
        user_parts: list[str] = []
        if accumulated_context:
            user_parts.append(f"Context from prior answers:\n{accumulated_context}\n")
        user_parts.append(f"Developer's answer:\n{user_answer}")
        user = "\n".join(user_parts)

        elaboration = llm_backend.complete(system=system, user=user, model_logical="default")
        elaborations.append((q_id, elaboration))

        # Accumulate context for subsequent questions
        accumulated_context += f"\n- {q_prompt}\n  {user_answer}\n"

    content = _render_hypothesis(elaborations)
    output_path = target_dir / "hypothesis.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    """Argparse CLI for the hypothesis scaffolder."""
    parser = argparse.ArgumentParser(
        prog="scaffolder",
        description="F4 /hypothesis --scaffold: interactive hypothesis builder",
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Directory where hypothesis.md will be written (default: .)",
    )
    parser.add_argument(
        "--backend",
        choices=["bedrock", "mock"],
        default="bedrock",
        help="LLM backend to use (default: bedrock)",
    )
    args = parser.parse_args(argv)

    backend: LLMBackend = MockBackend() if args.backend == "mock" else BedrockBackend()
    result = scaffold(target_dir=Path(args.target_dir), llm_backend=backend)
    print(f"hypothesis.md written to: {result}")


if __name__ == "__main__":
    main()
