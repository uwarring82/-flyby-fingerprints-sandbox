#!/usr/bin/env python3
"""Guardian gate for Simulation Report Standard (Phase 1)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List


def _find_latest_report(root: Path) -> Path:
    candidates = [
        path for path in root.iterdir() if path.is_dir() and (path / "guardian.json").exists()
    ]
    if not candidates:
        raise FileNotFoundError(f"No Guardian report folders found under {root}")
    return sorted(candidates)[-1]


def _load_guardian(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_guardian(guardian: dict) -> List[str]:
    errors: List[str] = []
    if not guardian.get("null_control_present"):
        errors.append("Null control missing or not flagged present")

    metrics = guardian.get("metrics", {})
    null_metrics = metrics.get("null", {})
    effect_metrics = metrics.get("effect", {})
    snr_metrics = metrics.get("snr", {})

    p_null = float(null_metrics.get("p_value", float("nan")))
    if not (p_null >= 0.05):
        errors.append(f"Null hypothesis test failed: p_null={p_null:.4g} < 0.05")

    effect_claimed = bool(effect_metrics.get("effect_claimed", False))
    if effect_claimed:
        p_effect = float(effect_metrics.get("p_value", float("nan")))
        if not (p_effect < 0.01):
            errors.append(
                f"Experimental vs null hypothesis test failed: p={p_effect:.4g} ≥ 0.01"
            )
        snr = float(snr_metrics.get("value", float("nan")))
        if not (snr >= 10.0):
            errors.append(f"SNR requirement failed: snr={snr:.3g} < 10")

    return errors


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Guardian simulation statistics")
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path("artifacts/reports"),
        help="Report directory or root containing multiple reports",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Treat the provided path as the exact report directory",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    target = args.path

    if args.exact:
        report_dir = target
    else:
        report_dir = target if (target / "guardian.json").exists() else _find_latest_report(target)

    guardian_path = report_dir / "guardian.json"
    guardian = _load_guardian(guardian_path)
    errors = _validate_guardian(guardian)

    if errors:
        for err in errors:
            print(f"Guardian veto: {err}", file=sys.stderr)
        return 1

    print(f"Guardian validation passed for {report_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
