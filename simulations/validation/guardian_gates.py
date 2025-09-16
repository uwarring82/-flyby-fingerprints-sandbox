from __future__ import annotations
import sys, json, pathlib
from dataclasses import dataclass
from typing import Any, List

ART = pathlib.Path("artifacts")
BASE = ART / "baseline"
DOCS_PHASE2 = pathlib.Path("docs/wiki/Phase_Gates/Phase_2_Integration.md")
DATA_META = pathlib.Path("data/metadata/datasets.yaml")


@dataclass
class GateResult:
    name: str
    passed: bool
    details: str = ""


def _read_json(p: pathlib.Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _phase2_enabled() -> bool:
    # Phase-2 enforcement toggles on when the Phase-2 gate page exists
    return DOCS_PHASE2.exists()


# ----------------- Phase 1 checks (kept) -----------------
def check_residuals_policy() -> GateResult:
    fp = ART / "residuals_summary.json"
    if not fp.exists():
        return GateResult("residuals_summary_present", False, "artifacts/residuals_summary.json not found")
    try:
        data = _read_json(fp)
    except Exception as e:
        return GateResult("residuals_summary_valid_json", False, f"error={e}")
    med = float(data.get("relative_medians", {}).get("rf_heating", 1.0))
    return GateResult("residuals_within_policy", med < 0.10, f"rf_heating_median={med}")


def check_uncertainty_documented() -> GateResult:
    missing = []
    bg = pathlib.Path("simulations/backgrounds")
    if not bg.exists():
        return GateResult("backgrounds_path_present", False, "simulations/backgrounds missing")
    for f in bg.glob("*.py"):
        if f.name == "__init__.py":
            continue
        txt = f.read_text(encoding="utf-8")
        if "Uncertainty" not in txt:
            missing.append(f.name)
    return GateResult("uncertainty_documented", not missing, f"missing={missing}")


def check_tests_path() -> GateResult:
    present = pathlib.Path("tests").exists()
    return GateResult("tests_path_present", present, "tests/ exists" if present else "tests/ missing")


# ----------------- Phase 2 checks (new) -----------------
def check_datasets_yaml_h_flags() -> GateResult:
    """
    Ensure every risk: H entry in datasets.yaml has requires_cross_validation: true.
    No external YAML dep: use a simple text fallback.
    """
    if not DATA_META.exists():
        return GateResult("datasets_yaml_present", False, "data/metadata/datasets.yaml missing")
    txt = DATA_META.read_text(encoding="utf-8")
    # Fallback heuristic: if any "risk: H" present, also require the flag string somewhere
    ok = ("risk: H" not in txt) or ("requires_cross_validation: true" in txt)
    det = "text-scan fallback; ensure all risk: H entries carry requires_cross_validation: true"
    return GateResult("h_risk_cross_validation_flags", ok, det)


def check_interaction_matrix(max_coupling: float = 0.10) -> GateResult:
    """
    Require interaction_matrix.json with coupling strengths <= 10%,
    or an INTERACTION_EXCEPTIONS.json mapping offenders -> mitigation notes.
    """
    if not BASE.exists():
        return GateResult("baseline_dir_present", False, "artifacts/baseline missing")
    im = BASE / "interaction_matrix.json"
    if not im.exists():
        return GateResult("interaction_matrix_present", False, f"{im} missing")
    try:
        M = _read_json(im)  # dict of {metric: coupling_strength}
    except Exception as e:
        return GateResult("interaction_matrix_valid_json", False, f"error={e}")
    offenders = {k: float(v) for k, v in M.items() if float(v) > max_coupling}
    if offenders:
        exc = BASE / "INTERACTION_EXCEPTIONS.json"
        if not exc.exists():
            return GateResult("interaction_couplings_within_threshold", False, f"offenders={offenders}; no exceptions file")
        try:
            ex_data = _read_json(exc)  # expect mitigations per offender key
        except Exception as e:
            return GateResult("interaction_exceptions_valid_json", False, f"error={e}")
        missing_mitigations = [k for k in offenders if k not in ex_data]
        return GateResult("interaction_couplings_with_mitigations", not missing_mitigations,
                          f"offenders={offenders}; missing_mitigations={missing_mitigations}")
    return GateResult("interaction_couplings_within_threshold", True, f"max<= {max_coupling}")


def check_benchmark_comparisons(min_refs: int = 3) -> GateResult:
    """
    Require benchmark_comparisons.json with >=3 independent references passing
    (either boolean True or dict {"pass": true, ...}).
    """
    fp = BASE / "benchmark_comparisons.json"
    if not fp.exists():
        return GateResult("benchmark_comparisons_present", False, f"{fp} missing")
    try:
        results = _read_json(fp)
    except Exception as e:
        return GateResult("benchmark_comparisons_valid_json", False, f"error={e}")
    passes = 0
    for _, v in results.items():
        if isinstance(v, bool) and v:
            passes += 1
        elif isinstance(v, dict) and bool(v.get("pass", False)):
            passes += 1
    return GateResult("benchmark_min_refs", passes >= min_refs, f"passes={passes} required>={min_refs}")


def main():
    results: List[GateResult] = [
        check_residuals_policy(),
        check_uncertainty_documented(),
        check_tests_path(),
    ]
    if _phase2_enabled():
        results += [
            check_datasets_yaml_h_flags(),
            check_interaction_matrix(),
            check_benchmark_comparisons(),
        ]
    for r in results:
        print(f"[GUARDIAN] {r.name}: {'PASS' if r.passed else 'FAIL'} :: {r.details}")
    if not all(r.passed for r in results):
        print("[GUARDIAN VETO] Safety criteria unmet.")
        sys.exit(2)
    print("[GUARDIAN] All safety checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
