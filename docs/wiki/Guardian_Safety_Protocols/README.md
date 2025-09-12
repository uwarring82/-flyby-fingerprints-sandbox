# Guardian Safety Protocols

## Purpose
Enforce protective standards across the flyby-fingerprints project and keep Phase gates auditable.

## Active Safety Requirements (MANDATORY)
1. **Uncertainty quantification** present in every physics module (e.g., `*Uncertainty` class + bounds helper).
2. **Guardian Safety Gate** must pass on CI for all merges to `main`.
3. **Residuals policy:** median relative residual `< 10%` for placeholder benchmarks (tighten when curated data lands).
4. **Failure Modes** are documented in model docs; validity ranges are explicit.
5. **H-risk interactions** carry `requires_cross_validation: true` in the interaction matrix.

## Review Cadence
- **Per-PR:** Automated Guardian gate on CI.
- **Weekly:** Manual Guardian review of physics modules and policies.
- **Phase Gates:** Tri-stance sign-off (Guardian / Architect / Integrator) before progressing.

## Evidence Artifacts
- CI logs showing **Smoketest** success and **Guardian Gate** PASS.
- `artifacts/residuals_summary.json` present on CI runs.
- Updated docs under `docs/wiki/` and model pages (e.g., `docs/rf_heating_model.md`).

## Current Status Snapshot (to be updated when Phase-1 closes)
- Phase: **Foundation**
- Guardian Gate: **PASS/FAIL**
- Residuals median (rf_heating): **<value from CI>**
- Next review: **<date>**
