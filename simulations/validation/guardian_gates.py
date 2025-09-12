from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import dataclass

ART = pathlib.Path("artifacts")
ART.mkdir(exist_ok=True, parents=True)


@dataclass
class GateResult:
    name: str
    passed: bool
    details: str = ""

def check_uncertainty_documented() -> GateResult:
    """Require the string 'Uncertainty' in each backgrounds module (except __init__.py)."""

    missing: list[str] = []
    for f in pathlib.Path("simulations/backgrounds").glob("*.py"):
        if f.name == "__init__.py":
            continue
        text = f.read_text(encoding="utf-8")
        if "Uncertainty" not in text:
            missing.append(f.name)
    return GateResult("uncertainty_documented", not missing, f"missing={missing}")


def check_tests_path() -> GateResult:
    """Pass only if a ``tests/`` directory exists."""

    exists = pathlib.Path("tests").is_dir()
    return GateResult("tests_path", exists, f"exists={exists}")


def check_residuals_policy() -> GateResult:
    """Require artifacts/residuals_summary.json with rf_heating median < 10%."""

    fp = ART / "residuals_summary.json"
    if not fp.exists():
        return GateResult("residuals_policy", False, "artifacts/residuals_summary.json not found")
    data = json.loads(fp.read_text(encoding="utf-8"))
    med = float(data.get("relative_medians", {}).get("rf_heating", 1.0))
    return GateResult("residuals_policy", med < 0.10, f"rf_heating_median={med}")


def main():
    checks = [check_uncertainty_documented, check_tests_path, check_residuals_policy]
    results = [fn() for fn in checks]
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[GUARDIAN] {r.name}: {status} :: {r.details}")
    if not all(r.passed for r in results):
        print("[GUARDIAN VETO] Safety criteria unmet.")
        sys.exit(2)
    print("[GUARDIAN] All safety checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
