"""F5 /spec-write — CLI entry point.

Usage:
    python -m primitives.spec_write.shared [target_dir] [--output PATH]
                                           [--dry-run] [--backend mock|bedrock]
                                           [--context TEXT]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from primitives._llm import BedrockBackend, MockBackend
from primitives.spec_write.shared import run
from primitives.spec_write.shared.interviewer import run_interview


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="spec-write",
        description=(
            "Interview-to-spec workflow. "
            "Asks 12 questions one at a time, drafts a 6-section spec.md, "
            "self-reviews for placeholders/contradictions/scope."
        ),
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Directory where spec.md will be written (default: current directory)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Override the output file path (default: {target_dir}/spec.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the drafted spec on stdout; do not write to disk",
    )
    parser.add_argument(
        "--backend",
        choices=["mock", "bedrock"],
        default="bedrock",
        help="LLM backend to use (default: bedrock)",
    )
    parser.add_argument(
        "--context",
        default="",
        help="Optional free-text context hint passed to the interviewer",
    )
    args = parser.parse_args()

    target_dir = Path(args.target_dir).resolve()
    output_path = Path(args.output).resolve() if args.output else target_dir / "spec.md"

    llm_backend = MockBackend() if args.backend == "mock" else BedrockBackend()

    answers = run_interview(llm_backend=llm_backend, context_hint=args.context)
    spec_text = run(
        answers=answers,
        output=output_path,
        dry_run=args.dry_run,
        llm_backend=llm_backend,
    )

    if args.dry_run:
        print(spec_text)
        return 0

    print(f"Spec written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
