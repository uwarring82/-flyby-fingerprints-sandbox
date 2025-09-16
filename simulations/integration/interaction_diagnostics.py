from __future__ import annotations
import json, os
from typing import Dict


def diagnose_interactions(
    individual: Dict[str, Dict[str, float]],
    combined: Dict[str, float],
    rel_threshold: float = 0.10,
    noise_floor: float = 1e-12,
) -> Dict[str, float]:
    """
    For each metric key k, compare combined[k] against sum_i individual[i][k].
    Returns dict of coupling strengths; also writes JSON for Guardian gating.

    strengths[k] = |combined[k] - Σ_i individual_i[k]| / max(|Σ_i individual_i[k]|, noise_floor)
    """
    strengths = {}
    keys = set(combined.keys())
    for m in individual.values():
        keys |= set(m.keys())

    for k in keys:
        s = sum(m.get(k, 0.0) for m in individual.values())
        denom = max(abs(s), noise_floor)
        c = abs(combined.get(k, 0.0) - s) / denom
        strengths[k] = float(c)

    os.makedirs("artifacts/baseline", exist_ok=True)
    with open("artifacts/baseline/interaction_matrix.json", "w", encoding="utf-8") as f:
        json.dump(strengths, f, indent=2)

    return {k: v for k, v in strengths.items() if v > rel_threshold}
