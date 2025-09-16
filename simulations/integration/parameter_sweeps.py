from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable

from simulations.integration.background_runner import run_baseline


def sweep(
    grid_omega_sec: Iterable[float],
    grid_pressure: Iterable[float],
    base_params: Dict[str, Any],
    refs: Dict[str, Any],
    out_path: str = "docs/validation_reports/phase2_dominance_maps/dominance_summary.json",
):
    os.makedirs("docs/validation_reports/phase2_dominance_maps", exist_ok=True)
    summary = []
    for w in grid_omega_sec:
        for P in grid_pressure:
            params = {**base_params, "omega_sec": w, "pressure": P}
            baseline = run_baseline(params, refs)
            summary.append({"omega_sec": w, "pressure": P, "rate": baseline["metrics"]["rate"]})
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary
