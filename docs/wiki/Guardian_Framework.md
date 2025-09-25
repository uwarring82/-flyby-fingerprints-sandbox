# Guardian Framework — Validation & Merge Gates

**Owner:** @uwarring82

**Phase-1 Exit Criteria**
- Background inventory complete (thermal, EM, surface, detection)
- Null controls pass (p ≥ 0.05)
- SNR ≥ 10 for claimed signatures
- Physics deviation < 0.1%
- I/O ground-truth preserved

**CI**
- `guardian-validation` job runs `pytest -q tests/guardian`
- Notebook smoke import check optional (`binder-badge-check.yml`)

**Certificates**
- Explorer exports JSON certificate (report + config snapshot) to `artifacts/notebook/`.
