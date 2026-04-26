"""Smoke tests for lab-4."""
from pathlib import Path
import re

LAB = Path(__file__).parent


def test_critique_exists():
    assert (LAB / "critique.md").exists()


def test_critique_status_valid():
    body = (LAB / "critique.md").read_text()
    m = re.search(r"^status:\s*(draft|complete)\s*$", body, re.MULTILINE)
    assert m and m.group(1) in {"draft", "complete"}


def test_starter_has_bad_prompts():
    body = (LAB / "starter" / "bad_prompts.md").read_text()
    numbered = [line for line in body.splitlines() if re.match(r"^\d+\.\s", line)]
    assert len(numbered) >= 4


def test_reference_answer_key_present():
    assert (LAB / "reference" / "answer-key.md").exists()
