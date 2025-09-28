# Simulation Report Standard (Phase 1, Guardian-compliant)

Every simulation run that produces publishable results **must** ship with a Guardian-compliant
report folder. Phase 1 locks down the non-negotiables so that any follow-on analysis can rely on
paired controls, statistical rigor, and immutable provenance.

## Mandatory checks per run

1. **Paired runs**: always generate an experimental dataset alongside a matched **null** dataset
   (physics disabled / collision pathways zeroed, same background settings).
2. **Statistics**: quantify the null and experimental comparison with at minimum:
   - Null-control hypothesis test (`p_null`)
   - Experimental vs null two-sided hypothesis test (`p_exp_vs_null`)
   - Claimed signatures must meet `SNR ≥ 10`
   - Report the effect size (Cohen's d) with a 95% confidence interval
3. **Immutable archival**:
   - Record the git commit hash for the generating code and note whether the tree was clean
   - Emit SHA-256 checksums for every artifact in the report bundle
   - Embed a `SIMULATION` watermark on all rendered plots/images
4. **Cross-validation hooks**:
   - Preserve enough metadata (environment, seeds, versions) for independent reproduction
   - Output structures must make it trivial to fan out to different platforms/engines

## Artifact bundle layout

Each run writes its outputs under `artifacts/reports/YYYYMMDD_HHMMSS_<shortsha>/` with the
following required files:

- `report.pdf` – human-readable summary (metrics, provenance, quick-look plots allowed)
- `metadata.json` – parameters, seeds, environment details, git SHA, tool versions
- `results.npz` – raw numeric arrays for experimental + null runs
- `guardian.json` – thresholds, p-values, effect size, SNR, inventory of controls
- `sha256sum.txt` – SHA-256 checksums for every file in the directory
- `code_state.txt` – git commit SHA and clean-tree flag captured at runtime
- `*_time_series.png`, `*_psd.png`, `*_allan.png` – PNG plots with a `SIMULATION` watermark

Additional plots or tables may be included, but the above files are non-negotiable. Any auxiliary
artifacts must also be covered by the checksum manifest.

## Statistical thresholds (Phase 1)

- **Null control**: the null dataset must *fail to reject* the null hypothesis with `p_null ≥ 0.05`
- **Experimental vs null**: when an effect is claimed, report a two-sided p-value satisfying
  `p_exp_vs_null < 0.01`
- **Signal-to-noise ratio**: any claimed signal must meet or exceed `SNR ≥ 10`
- **Effect size**: report Cohen's d and its 95% confidence interval for transparency

If any of the above checks fail, the run is non-compliant and **cannot** be published or merged.

## Guardian gate

Guardian automation consumes `guardian.json` and blocks merges when:

- A null control is missing or flagged as failing
- `p_null < 0.05`
- `p_exp_vs_null ≥ 0.01` for claimed effects
- `SNR < 10` for claimed signals

The CI workflow `simulation-validation` runs a smoke simulation and applies the validator. Treat
any failures as a Guardian veto that must be resolved before landing changes.
