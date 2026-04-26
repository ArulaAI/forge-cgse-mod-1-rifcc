"""Dispatch entry point for the F4 hypothesis primitive.

Invoked as ``python3 -m primitives.hypothesis.shared <mode> [args...]``

Modes
-----
--scaffold <target_dir> [--backend bedrock|mock]
    Interactive hypothesis builder.  Writes hypothesis.md to <target_dir>.

--validate <hypothesis_file> --evidence <text> [--backend bedrock|mock]
    Evaluate evidence against an existing hypothesis.md.
"""

from __future__ import annotations

import sys

from primitives.hypothesis.shared.scaffolder import main as scaffold_main
from primitives.hypothesis.shared.validator import main as validate_main


def main() -> None:  # pragma: no cover
    """Route --scaffold / --validate to the appropriate module CLI."""
    args = sys.argv[1:]
    if not args:
        print(
            "Usage: python3 -m primitives.hypothesis.shared --scaffold <path> | "
            "--validate <path> --evidence <text>",
            file=sys.stderr,
        )
        sys.exit(1)

    mode = args[0]
    remaining = args[1:]

    if mode == "--scaffold":
        scaffold_main(remaining)
    elif mode == "--validate":
        validate_main(remaining)
    else:
        print(f"ERROR: unknown mode '{mode}'. Use --scaffold or --validate.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
