# Simulation Report Standard (Phase 1)

This project enforces Guardian-grade reproducibility for every simulation run:

- **Paired runs**: always produce both an experimental dataset and a matched **null** run with physics disabled (collision pathways zeroed) but identical backgrounds.
- **Statistics**: null-control p-value must satisfy `p ≥ 0.05`; experimental vs null two-sided p-value must be `< 0.01` when claiming an effect; any claimed signal requires `SNR ≥ 10`; report Cohen's d with a 95% confidence interval.
- **Immutable artifacts**: capture git SHA, clean-tree flag, and SHA-256 checksums; watermark all plots with `SIMULATION`.
- **Outputs**: each run drops a PDF report, metadata JSON, NPZ arrays, Guardian metrics, and plots under `artifacts/reports/<timestamp>_<sha>/`.

See the repository's [`REPORTING.md`](../../REPORTING.md) for the authoritative checklist and file-level requirements. Continuous integration runs a smoke simulation and rejects pull requests that violate the validator.
