"""Tests for /walk-rifcc."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from walker import LETTERS, emit_journey_event, render_check_only, render_markdown, walk


def test_walk_returns_5_letters():
    w = walk("review my refactor")
    assert len(w.letters) == 5
    assert set(w.letters.keys()) == set(LETTERS)


def test_render_markdown_lists_all_letters():
    w = walk("review my refactor")
    md = render_markdown(w)
    for letter in LETTERS:
        assert letter in md


def test_check_only_one_line():
    w = walk("review my refactor")
    line = render_check_only(w)
    assert "\n" not in line


def test_journey_event(tmp_path: Path):
    w = walk("review my refactor")
    (tmp_path / ".forge").mkdir()
    journey = tmp_path / ".forge" / "journey"
    target = emit_journey_event(w, journey_dir=journey)
    assert target.exists()
    payload = json.loads(target.read_text().strip().splitlines()[-1])
    assert payload["event"] == "walk_rifcc_run"
    assert payload["letters_walked"] == 5


def test_letters_are_canonical():
    assert LETTERS == ("Role", "Intent", "Frame", "Constraints", "Confidence")
