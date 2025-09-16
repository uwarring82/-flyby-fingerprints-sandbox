from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulations.integration.parameter_sweeps import sweep

refs = {
    "nist2016_heating": {"value": 1.00, "sigma": 0.15},
    "innsbruck2018_rates": {"value": 1.10, "sigma": 0.10},
    "umd2019_micromotion": {"value": 0.90, "sigma": 0.10},
}
base = {"mass": 2.29e-25, "T": 300.0, "S_E0": 2.36e-8}
w = [2*math.pi*1.0e6, 2*math.pi*1.5e6]
P = [3e-9, 1e-8]

if __name__ == "__main__":
    sweep(w, P, base, refs)
    print("[SWEEP] Wrote docs/validation_reports/phase2_dominance_maps/dominance_summary.json")
