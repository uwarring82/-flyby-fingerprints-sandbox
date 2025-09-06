SPDX-License-Identifier: GPL-3.0-or-later

# Data & Workflow

## Current status: simulated datasets (sandbox)
The repo ships **sandbox** datasets only (not experimental). See `DATASETS.md` for formats and quick start.

**Schema (CSV):**
- `heating.csv`: trap_id, run_id, mode, frequency_hz, heating_rate_quanta_per_s, heating_rate_err
- `sb_trials.csv`: trap_id, run_id, sequence, outcome (0/1), t_rel_s
- `events.csv`: trap_id, run_id, t_s

## Running the Fast Triad
```bash
python scripts/run_triad.py --data-root data-sandbox/clean --out out
```

Outputs: `out/triad_summary.csv`, `out/triad_report.json`, and `out/plots/*.png`.

Reproducibility
- Environment via `environment.yml` (conda) or `requirements.txt` (pip)
- CI to validate schema/analysis (optional)
- Pre-registration of thresholds and windowing for consistency
