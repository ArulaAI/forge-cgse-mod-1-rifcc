"""F5 /spec-write — one-question-at-a-time interview loop.

Iterates interview_questions.yaml (12 questions), passes each question + all prior
answers as the system message context, calls the LLM backend once per question,
returns the ordered list of InterviewAnswer objects.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from pydantic import BaseModel

if TYPE_CHECKING:
    from primitives._llm import LLMBackend

_QUESTIONS_PATH = Path(__file__).parent / "interview_questions.yaml"


class InterviewAnswer(BaseModel):
    """One answer from the interview loop."""

    question_id: str
    question_text: str
    answer: str


def _load_questions() -> list[dict[str, str]]:
    """Load the ordered question bank from interview_questions.yaml."""
    data = yaml.safe_load(_QUESTIONS_PATH.read_text())
    return list(data["questions"])


def run_interview(
    llm_backend: LLMBackend,
    context_hint: str = "",
    answers_override: list[str] | None = None,
) -> list[InterviewAnswer]:
    """Ask all 12 questions in order, accumulating context.

    Args:
        llm_backend: LLM backend (MockBackend or BedrockBackend).
        context_hint: Optional free-text hint prepended to the system prompt for
                      every question (e.g. "Lab 3 — caching exercise").
        answers_override: If provided, these strings are used as the raw user input
                          for each question (used in tests to avoid interactive prompts).
                          Must be the same length as the question bank or it will cycle.

    Returns:
        Ordered list of InterviewAnswer objects, one per question.
    """
    questions = _load_questions()
    accumulated: list[InterviewAnswer] = []

    for idx, q in enumerate(questions):
        # Build system message: context hint + all prior answers
        prior_text = ""
        if accumulated:
            prior_lines = [f"Q: {a.question_text}\nA: {a.answer}" for a in accumulated]
            prior_text = "\n\n".join(prior_lines)

        system_parts: list[str] = []
        if context_hint:
            system_parts.append(f"Context: {context_hint}")
        system_parts.append(q["prompt"])
        if prior_text:
            system_parts.append(f"\n\nPrevious answers for context:\n{prior_text}")
        system = "\n".join(system_parts)

        # User message: the raw answer text (interactive or overridden)
        if answers_override is not None:
            raw_answer = answers_override[idx % len(answers_override)]
        else:
            raw_answer = ""

        # LLM call — in interactive mode the user types; here we pass the raw answer
        # through the LLM to allow elaboration/clarification.
        elaborated = llm_backend.complete(system=system, user=raw_answer, model_logical="default")

        accumulated.append(
            InterviewAnswer(
                question_id=q["id"],
                question_text=q["prompt"],
                answer=elaborated,
            )
        )

    return accumulated
