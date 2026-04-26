"""F5 /spec-write — LLM-driven spec.md composer.

Loads the spec_template.md skeleton, assembles all 12 interview answers into a
structured prompt, calls the LLM backend once, and returns the rendered spec as a
Markdown string.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from primitives._llm import LLMBackend

from primitives.spec_write.shared.interviewer import InterviewAnswer

_TEMPLATE_PATH = Path(__file__).parent / "spec_template.md"

_SYSTEM_PROMPT = """\
You are a technical writer producing a structured spec.md document.

You will receive a set of interview answers from a developer. Using those answers,
produce a complete, well-written spec.md following the template structure below.
Fill every section with substantive content drawn from the answers.
Return ONLY the spec.md Markdown — no preamble, no explanation.

Required sections (all six must be present):
1. ## Goal
2. ## Architecture
3. ## File structure
4. ## Acceptance criteria
5. ## Risks
6. ## Decision log

Template for reference:
{template}
"""


def _build_user_message(answers: Sequence[InterviewAnswer]) -> str:
    lines = ["Interview answers:"]
    for a in answers:
        lines.append(f"\n[{a.question_id}] {a.question_text}")
        lines.append(f"Answer: {a.answer}")
    return "\n".join(lines)


def draft_spec(
    answers: Sequence[InterviewAnswer],
    llm_backend: LLMBackend,
) -> str:
    """Compose the spec.md from interview answers via a single LLM call.

    Args:
        answers: Ordered list of InterviewAnswer (typically 12, but shorter lists
                 are accepted — the LLM will fill missing sections with placeholders).
        llm_backend: LLM backend (MockBackend or BedrockBackend).

    Returns:
        The rendered spec.md content as a Markdown string.
    """
    template_text = _TEMPLATE_PATH.read_text()
    system = _SYSTEM_PROMPT.format(template=template_text)
    user = _build_user_message(answers)
    return llm_backend.complete(system=system, user=user, model_logical="default")
