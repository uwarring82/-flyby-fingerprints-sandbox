#!/usr/bin/env python3
"""Run formatting and linting checks.

This gate ensures code is formatted and linted by invoking
Black and Ruff. It exits with a non-zero code if either tool fails.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys


TARGETS = ["simulations", "tests", "docs", "examples", "tools"]
COMMANDS: list[list[str]] = [
    ["black", "--check", "--diff", *TARGETS],
    ["ruff", "check", *TARGETS],
]


def main() -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    failures: list[str] = []
    for cmd in COMMANDS:
        print("+", " ".join(cmd))
        result = subprocess.run(cmd, cwd=root)
        if result.returncode != 0:
            failures.append(cmd[0])
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
