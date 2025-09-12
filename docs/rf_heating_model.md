# RF Heating Model

This document describes the RF heating background model. [1][2][3]

<!-- TODO: Add model description and references -->

## Validity Range
This model assumes a power-law electric-field noise spectrum with stationary statistics.
The **validated frequency range** is **f ∈ [1e5, 1e7] Hz** (from `RFHeatingUncertainty.validity_range_hz`).
Outside this range, results are **extrapolations** and must be tagged as such in analysis outputs.

## Failure Modes and Mitigations

### Non-stationary Noise
- **Symptom:** Heating rate drifts >20% over 10–30 min windows.
- **Detection:** Sliding-window estimator with SPC thresholds.
- **Mitigation:** Adaptive noise-floor tracking; segmented analysis.

### Coherent Pickup
- **Symptom:** Narrow spectral lines >3σ above continuum.
- **Detection:** FFT of field-noise estimate with line tracking.
- **Mitigation:** Notch filtering; RF hygiene (grounds, cable routing).

### Unknown-Mode Protocol
If residual trends persist after mitigations, trigger **Level-2 Guardian Review** and require an alternate model cross-check before merging.
