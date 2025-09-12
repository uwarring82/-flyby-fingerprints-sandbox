"""Basic Guardian gate checks for CI."""

from __future__ import annotations

import json
import pathlib
import sys


DATASETS = pathlib.Path("data/metadata/datasets.yaml")
RESIDUALS = pathlib.Path("artifacts/residuals_summary.json")


def check_canonical_dataset() -> bool:
    if DATASETS.exists():
        print("PASS: datasets metadata present")
        return True
    print("FAIL: missing datasets metadata")
    return False


def check_residuals_artifact() -> bool:
    if RESIDUALS.exists():
        try:
            json.loads(RESIDUALS.read_text() or "{}")
            print("PASS: residuals summary present")
            return True
        except json.JSONDecodeError as exc:
            print(f"FAIL: residuals summary invalid JSON: {exc}")
            return False
    print("FAIL: residuals summary missing")
    return False


def main() -> None:
    checks = [check_canonical_dataset(), check_residuals_artifact()]
    if not all(checks):
        sys.exit(1)
    print("All guardian gates passed.")


if __name__ == "__main__":  # pragma: no cover
    main()
