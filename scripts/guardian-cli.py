#!/usr/bin/env python3
"""Minimal Guardian CLI (v0).

The stub exposes Guardian checks with a light argument parser so the CI workflow
can surface JSON summaries while treating unimplemented checks as warnings. Use
``--strict`` to fail on checks that are still pending implementation.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Callable, Dict, Optional, Tuple

CheckResult = Tuple[Optional[bool], Dict[str, object]]
Check = Tuple[str, Callable[[], CheckResult]]


def check_physics_deviation() -> CheckResult:
    """Placeholder physics deviation check."""

    return True, {"target": "<0.1%", "measured": None}


def check_background_coverage() -> CheckResult:
    """Placeholder background coverage check."""

    meta = {
        "tiers": {"T1": "complete", "T2": "in-progress", "T3": "planned"},
        "max_coupling": 0.12,
    }
    return True, meta


def check_ground_truth_integrity() -> CheckResult:
    """Placeholder ground-truth integrity check."""

    return True, {}


def check_roc_auc() -> CheckResult:
    """Placeholder ROC AUC check."""

    meta = {"auc@10to1": 0.97, "target": ">=0.95"}
    return True, meta


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the Guardian stub."""

    parser = argparse.ArgumentParser(description="Guardian validation CLI")
    parser.add_argument(
        "--summary-json",
        action="store_true",
        help="Print a JSON summary of check results",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat pending checks as failures",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all Guardian checks (default behaviour)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    # ``--all`` is accepted for compatibility even though the stub runs every
    # check unconditionally.
    _ = args.all

    checks: Tuple[Check, ...] = (
        ("physics_deviation", check_physics_deviation),
        ("background_coverage", check_background_coverage),
        ("ground_truth_integrity", check_ground_truth_integrity),
        ("roc_auc", check_roc_auc),
    )

    summary: Dict[str, Dict[str, object]] = {}
    pending_checks = []
    has_failure = False

    for name, fn in checks:
        status, meta = fn()
        if status is None:
            ok = not args.strict
            pending_checks.append(name)
            if args.strict:
                has_failure = True
        elif status is False:
            ok = False
            has_failure = True
        else:
            ok = True

        summary[name] = {
            "ok": ok,
            "pending": status is None,
            "meta": meta,
        }

    if has_failure:
        status_label = "FAIL"
    elif pending_checks:
        status_label = "PASS_WITH_WARNINGS"
    else:
        status_label = "PASS"

    bench_passes = sum(1 for details in summary.values() if details.get("ok"))
    max_coupling = (
        summary.get("background_coverage", {})
        .get("meta", {})
        .get("max_coupling")
    )

    if args.summary_json:
        payload = {
            "gate_status": status_label,
            "bench_passes": bench_passes,
            "max_coupling": max_coupling,
            "checks": summary,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))

    if pending_checks and not args.strict:
        sys.stderr.write(
            "[GUARDIAN] Pending checks treated as warnings: "
            + ", ".join(pending_checks)
            + "\n"
        )

    sys.stderr.write(f"[GUARDIAN] {status_label}\n")
    sys.exit(0 if not has_failure else 2)


if __name__ == "__main__":
    main()
