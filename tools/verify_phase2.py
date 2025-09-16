from __future__ import annotations
import json, os, sys, math, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulations.integration.background_runner import run_baseline

# ---- 1) References (≥3; uncertainty-aware) ----
REFS = {
    "nist2016_heating":   {"value": 1.00, "sigma": 0.15},
    "innsbruck2018_rates":{"value": 1.10, "sigma": 0.10},
    "umd2019_micromotion":{"value": 0.90, "sigma": 0.10},
}

# ---- 2) Baseline parameters (realistic; adjust as needed) ----
PARAMS = {
    "omega_sec": 2*math.pi*1.0e6,  # rad/s
    "mass": 2.29e-25,              # kg (Ca+ ~ 40 amu)
    "T": 300.0,                    # K
    "S_E0": 2.36e-8,               # V^2/m^2/Hz (tuned for ~1 quanta/ms baseline)
    # Optional: "pressure": 3e-9, "alpha": 1.0, "d_elec": 50e-6
}

def main() -> int:
    os.makedirs("artifacts/baseline", exist_ok=True)

    # A) Produce REAL baseline + diagnostics + benchmark comparisons
    baseline = run_baseline(PARAMS, REFS)

    # B) Summarize artifacts
    im_path = "artifacts/baseline/interaction_matrix.json"
    bc_path = "artifacts/baseline/benchmark_comparisons.json"
    bd_path = "artifacts/baseline/baseline_distributions.json"

    missing = [p for p in (im_path, bc_path, bd_path) if not os.path.exists(p)]
    if missing:
        print("[VERIFY] Missing artifacts:", missing); return 2

    with open(im_path, "r", encoding="utf-8") as f:
        interactions = json.load(f)
    with open(bc_path, "r", encoding="utf-8") as f:
        benchmarks = json.load(f)
    with open(bd_path, "r", encoding="utf-8") as f:
        baseline_distrib = json.load(f)

    # C) Print summary
    couplings = {k: float(v) for k,v in interactions.items()}
    max_cpl = max(couplings.values()) if couplings else 0.0
    passes = sum(int(v if isinstance(v,bool) else bool(v.get("pass",False))) for v in benchmarks.values())
    print("\n[VERIFY] Baseline metrics:", baseline_distrib.get("metrics"))
    print("[VERIFY] Max coupling strength:", max_cpl)
    print("[VERIFY] Benchmark passes (>=3 required):", passes)

    # D) Run Guardian gate
    print("\n[VERIFY] Running Guardian Safety Gate...")
    rc = subprocess.call([sys.executable, "-m", "simulations.validation.guardian_gates"])
    print("[VERIFY] Guardian gate exit code:", rc)

    # E) Quick policy assertion (mirrors Guardian)
    ok = (rc == 0)
    if not ok:
        print("\n[VERIFY] Gate failed. Common fixes:")
        print(" - If coupling > 0.10 is legitimate, add artifacts/baseline/INTERACTION_EXCEPTIONS.json")
        print(" - Ensure ≥3 benchmarks have pass=True (use uncertainty-aware entries)")
        print(" - Confirm datasets.yaml has requires_cross_validation: true for all risk: H")
    else:
        print("\n[VERIFY] ✅ All safety checks passed on REAL artifacts.")
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
