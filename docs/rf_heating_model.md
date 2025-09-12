# RF Heating Model

This document describes the RF heating background model. [1][2][3]

<!-- TODO: Add model description and references -->

## Failure Modes and Mitigations

### Non-stationary Noise
- **Symptom**: Heating rate drifts >20% over 10–30 min windows
- **Detection**: Sliding-window estimator with SPC thresholds
- **Mitigation**: Adaptive noise-floor tracking; segment analysis

### Coherent Pickup
- **Symptom**: Spectral lines >3σ above continuum
- **Detection**: FFT of field-noise estimate; line-tracking
- **Mitigation**: Notch filtering; cable/grounding review; RF hygiene

### Unknown Mode Protocol
- **Trigger**: Residual trends persist post-mitigation
- **Action**: Level-2 Guardian Review; require alternate model cross-check
