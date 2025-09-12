
# Sandbox Datasets

This repository provides **simulated datasets** (sandbox only) to demonstrate the analysis workflow.
These are *not experimental data* but synthetic examples generated for testing and reproducibility.

---

## Quick Start Example

A small clean dataset is provided directly in the repository under [`data-sandbox/`](data-sandbox/).
It contains three CSV files in the expected format:

- `heating.csv` — heating-rate measurements vs frequency
- `sb_trials.csv` — interleaved binary trial outcomes (RSB/BSB or dark/bright)
- `events.csv` — event timestamps (outliers/jumps)

This dataset allows visitors to immediately inspect the structure and try the analysis without any extra steps.

Usage:
```bash
python adm_fast_triad.py --data-root data-sandbox/clean --out out/
```

---

## Extended Sandbox Datasets

For larger or more varied runs, we also provide zipped archives in `datasets/`:

- **`sandbox_clean_dataset.zip`** — background-only simulation
- **`sandbox_flyby_dataset.zip`** — includes simulated fly-by (residual-gas) fingerprints

Unzip them into a working folder (e.g. `data/`) to run the full pipeline.

Example:
```bash
unzip datasets/sandbox_flyby_dataset.zip -d data/
python adm_fast_triad.py --data-root data/flyby --out out/
```

---

## Notes

- These datasets are fully synthetic and intended only for sandbox testing.
- Real experimental data should follow the same CSV schema.
- Contributions of additional sandbox scenarios are welcome, provided they are clearly labeled as simulated.

