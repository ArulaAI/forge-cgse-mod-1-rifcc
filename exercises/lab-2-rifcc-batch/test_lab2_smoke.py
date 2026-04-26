"""Smoke tests for lab-2."""
from pathlib import Path
import re

LAB = Path(__file__).parent


def test_spec_and_hypothesis_exist():
    assert (LAB / "spec.md").exists() and (LAB / "hypothesis.md").exists()


def test_spec_status_valid():
    body = (LAB / "spec.md").read_text()
    m = re.search(r"^status:\s*(draft|complete)\s*$", body, re.MULTILINE)
    assert m and m.group(1) in {"draft", "complete"}


def test_starter_asks_present():
    asks = (LAB / "starter" / "asks.md").read_text()
    # Count numbered list lines
    numbered = [line for line in asks.splitlines() if re.match(r"^\d+\.\s", line)]
    assert len(numbered) >= 5
