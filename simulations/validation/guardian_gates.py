from __future__ import annotations
import sys, json, pathlib, ast
from dataclasses import dataclass

ART = pathlib.Path("artifacts")
ART.mkdir(exist_ok=True, parents=True)


@dataclass
class GateResult:
    name: str
    passed: bool
    details: str = ""

def check_uncertainty_documented() -> GateResult:
    """Require an *Uncertainty class in each backgrounds module (except __init__.py)."""
    missing = []
    for f in pathlib.Path("simulations/backgrounds").glob("*.py"):
        if f.name == "__init__.py":
            continue
        tree = ast.parse(f.read_text(encoding="utf-8"))
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        if not any("Uncertainty" in c for c in classes):
            missing.append(f.name)
    return GateResult("uncertainty_documented", not missing, f"missing={missing}")


def check_tests_exist() -> GateResult:
    tests = list(pathlib.Path("tests").glob("test_*.py"))
    return GateResult("tests_exist", len(tests) > 0, f"found={len(tests)}")


def check_residuals_policy() -> GateResult:
    """Require a residuals summary JSON with median relative residuals < 10% for RF baseline."""
    fp = ART / "residuals_summary.json"
    if not fp.exists():
        return GateResult("residuals_summary_present", False, "artifacts/residuals_summary.json not found")
    data = json.loads(fp.read_text(encoding="utf-8"))
    med = float(data.get("relative_medians", {}).get("rf_heating", 1.0))
    return GateResult("residuals_within_policy", med < 0.10, f"rf_heating_median={med}")


def main():
    checks = [check_uncertainty_documented, check_tests_exist, check_residuals_policy]
    results = [fn() for fn in checks]
    for r in results:
        print(f"[GUARDIAN] {r.name}: {'PASS' if r.passed else 'FAIL'} :: {r.details}")
    if not all(r.passed for r in results):
        print("[GUARDIAN VETO] Safety criteria unmet.")
        sys.exit(2)
    print("[GUARDIAN] All safety checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
