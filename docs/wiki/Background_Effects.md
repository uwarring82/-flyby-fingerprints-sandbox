# Background Effects — Implementations & Fingerprints

**Implemented (stubs ready for refinement):**
- Thermal secular motion proxy (`thermal_motion.py`)
- EM pickup (mains + broadband) (`em_artifacts.py`)
- Surface drift (random-walk proxy) (`surface_effects.py`)
- Detection noise (Poisson) (`detection_noise.py`)

**Explorer Notebook:** `Background_Model_Explorer.ipynb` (Binder/Voilà links in README and docs)

## What to Look For
- **EM PSD:** mains peaks; broadband floor
- **Surface drift:** monotonic low-freq wander; Allan-like variance ↑ with τ
- **Detector counts:** Poisson GOF (null ≥ 0.05)

## Next Up
- PSD regression tests for RF pickup
- Allan-variance thresholding for drift
- Parameter calibration presets + Guardian certificate baselines
