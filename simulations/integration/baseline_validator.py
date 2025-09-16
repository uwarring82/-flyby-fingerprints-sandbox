from __future__ import annotations
import json, os
from typing import Dict, Union

Ref = Union[float, Dict[str, float]]  # float or {"value": x, "sigma": s}


def validate_baseline(
    baseline: Dict[str, float],
    references: Dict[str, Ref],
    rel_tolerance: float = 0.20,
    sigma_N: float = 2.0,
) -> Dict[str, dict]:
    """
    Compare baseline vs references; uncertainty-aware passes allowed.
    Returns {ref_id: {"pass": bool, "dev": float, "sigma": float or None}}
    """
    report = {}
    for key, ref in references.items():
        sim = baseline.get(key, None)
        if sim is None:
            report[key] = {"pass": False, "dev": None, "sigma": None, "reason": "missing_sim_value"}
            continue
        if isinstance(ref, dict) and "value" in ref:
            val = float(ref["value"])
            sigma = float(ref.get("sigma", 0.0))
            dev = abs(sim - val) / max(abs(val), 1e-12)
            tol_sigma = (sigma_N * sigma) / max(abs(val), 1e-12) if sigma > 0 else 0.0
            passed = dev <= max(rel_tolerance, tol_sigma)
            report[key] = {"pass": bool(passed), "dev": float(dev), "sigma": float(sigma)}
        else:
            val = float(ref)
            dev = abs(sim - val) / max(abs(val), 1e-12)
            report[key] = {"pass": bool(dev <= rel_tolerance), "dev": float(dev), "sigma": None}

    os.makedirs("artifacts/baseline", exist_ok=True)
    with open("artifacts/baseline/benchmark_comparisons.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return report
