from simulations.integration.background_runner import run_baseline

refs = {
    "nist2016_heating": {"value": 1.0, "sigma": 0.15},
    "innsbruck2018_rates": {"value": 1.1, "sigma": 0.10},
    "umd2019_micromotion": {"value": 0.9, "sigma": 0.10},
}

params = {
    "omega_sec": 2 * 3.14159e6,
    "mass": 2.29e-25,
    "T": 300.0,
    "S_E0": 2.5e-8,
    # "pressure": 3e-9, "alpha": 1.0, "d_elec": 50e-6, ...
}

if __name__ == "__main__":
    bl = run_baseline(params, refs)
    print("[Phase-2] Baseline generated:", bl["metrics"])
