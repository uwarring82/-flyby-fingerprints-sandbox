# flyby-fingerprints-sandbox

Sandbox environment for analyzing heating-rate datasets of trapped ions to identify **fingerprints of fly-by (residual-gas) collisions**.
This project provides tools to reanalyse historical data using the **Fast Triad (A–D–M) pilot**, a three-perspective framework for detecting weak collisions:

- **Analog (A):** Heating-rate scaling vs. trap frequency.
- **Digital (D):** Burstiness and clustering in binary RSB/BSB trial outcomes.
- **Memory (M):** Short-lag correlations in event-time series.

The approach is inspired by error-detection principles: combining three independent perspectives for fast checks, with the option to expand to a full seven-perspective analysis and multi-lab network protocols.

---

## Getting Started

### Requirements
- Python 3.10+

### Option 1: pip
Install dependencies via:
```bash
pip install -r requirements.txt
```

### Option 2: conda
A `environment.yml` is provided for reproducibility. Create the environment with:
```bash
conda env create -f environment.yml
conda activate flyby-fingerprints
```

### Data Format
The analysis expects three input files in `data/`:

1. **`heating.csv`**
   Heating-rate measurements vs. frequency.
   Columns: `trap_id, run_id, mode, frequency_hz, heating_rate_quanta_per_s, heating_rate_err`.

2. **`sb_trials.csv`**
   Interleaved sideband (or equivalent) binary outcome trials.
   Columns: `trap_id, run_id, sequence, outcome, t_rel_s`.

3. **`events.csv`**
   Event timestamps (jumps, outliers).
   Columns: `trap_id, run_id, t_s`.

### Running the Analysis
```bash
python adm_fast_triad.py --data-root data --out out
```

Outputs:
- `out/triad_summary.csv`: per-run statistics and triad decisions.
- `out/triad_report.json`: summary of flagged runs.

---

## Roadmap
- Extend to full seven-perspective (heptad) analysis.
- Combine results across multiple labs in a 7×7 product-code network structure.
- Provide a public data submission workflow (community contributions).

---

## Contributing
Contributions are welcome — please open issues or pull requests.
All contributors must agree that their code and data are released under **GPLv3**.

---

## License
This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.
You are free to use, modify, and distribute this code, provided that any derivative work is also released under the same license.

See the [LICENSE](LICENSE) file for details.
