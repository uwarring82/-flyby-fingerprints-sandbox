SPDX-License-Identifier: GPL-3.0-or-later

# Underlying Physics (brief)

## Trapped-ion heating: backgrounds vs. fly-by collisions
Motional heating in RF Paul traps can arise from:
- **Electric-field noise / patch potentials** — typically modeled as power-law spectral densities, often decreasing with frequency and electrode-ion distance.
- **Fly-by (residual-gas) collisions** — impulsive momentum kicks from dilute background gas, weakly frequency-dependent when averaged over modes, and potentially clustered in time if pressure fluctuates.

### Expected fingerprints
- **A (Analog):** Deviation from a pure power-law Γ̇(ω) via a small additive (weakly ω-dependent) term consistent with rare impulses.
- **D (Digital):** Overdispersion and abnormal run structure in binary outcomes (e.g., RSB/BSB), reflecting bursty intervals.
- **M (Memory):** Short-lag autocorrelation above white-noise baselines in event counts (e.g., Ljung–Box significance; characteristic Allan-variance slope).

### Confounders & controls
- Micromotion (RF), laser scatter, servo or digitizer artifacts, pressure/temperature drift, analysis pipeline bias. Mitigate via pre-registration, blinding of toggles, hardware heterogeneity, and end-to-end synthetic injections.

For deeper background, see [References](References.md).
