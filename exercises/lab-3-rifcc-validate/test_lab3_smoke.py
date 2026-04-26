"""Smoke tests for lab-3."""
from pathlib import Path
import re

LAB = Path(__file__).parent


def test_spec_and_hypothesis_exist():
    assert (LAB / "spec.md").exists() and (LAB / "hypothesis.md").exists()


def test_spec_status_valid():
    body = (LAB / "spec.md").read_text()
    m = re.search(r"^status:\s*(draft|complete)\s*$", body, re.MULTILINE)
    assert m and m.group(1) in {"draft", "complete"}


def test_instructions_demands_validation():
    body = (LAB / "instructions.md").read_text()
    assert "FM4" in body
