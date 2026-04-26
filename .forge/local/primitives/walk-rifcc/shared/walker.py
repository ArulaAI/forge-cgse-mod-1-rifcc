"""walk-rifcc — canonical F8 reference impl."""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path


LETTERS = ("Role", "Intent", "Frame", "Constraints", "Confidence")


@dataclass
class Walked:
    ask: str
    letters: dict[str, str]


def walk(ask: str) -> Walked:
    return Walked(ask=ask, letters={letter: f"<fill in {letter} for: {ask}>" for letter in LETTERS})


def render_markdown(w: Walked) -> str:
    lines = [f"# /walk-rifcc — `{w.ask}`", ""]
    for letter in LETTERS:
        lines.append(f"## {letter}")
        lines.append(w.letters[letter])
        lines.append("")
    return "\n".join(lines) + "\n"


def render_check_only(w: Walked) -> str:
    return f"walk-rifcc: ask=\"{w.ask[:40]}...\" letters_walked={len(w.letters)}"


def emit_journey_event(w: Walked, journey_dir: Path | None = None) -> Path | None:
    journey_dir = journey_dir or Path(".forge/journey")
    if not journey_dir.parent.exists():
        return None
    journey_dir.mkdir(parents=True, exist_ok=True)
    run_id = os.environ.get("FORGE_RUN_ID") or uuid.uuid4().hex
    target = journey_dir / f"{run_id}.jsonl"
    event = {
        "ts": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "event": "walk_rifcc_run",
        "ask": w.ask,
        "letters_walked": len(w.letters),
    }
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="walk-rifcc")
    parser.add_argument("ask", nargs="+")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--journey-dir", default=None)
    args = parser.parse_args(argv)
    ask = " ".join(args.ask)
    w = walk(ask)
    emit_journey_event(w, Path(args.journey_dir) if args.journey_dir else None)
    if args.check_only:
        print(render_check_only(w))
    else:
        print(render_markdown(w), end="")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
