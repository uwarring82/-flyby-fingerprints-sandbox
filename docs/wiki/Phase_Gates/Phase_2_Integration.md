# Phase-2: Integration Gate

## Completion Requirements
- [ ] Background interaction matrix documented (coupling strengths ≤ 10% or mitigations recorded)
- [ ] Baseline validation against ≥3 independent literature datasets (deviation < 20% or within 2σ)
- [ ] Parameter constraints documented and enforced (see data/metadata/physical_constraints.json)
- [ ] Regression checks: integrated vs individual modules consistent when others disabled
- [ ] Uncertainty propagation includes correlation notes (doc excerpt or derivation)

## Sign-offs (Tri-stance)
- Guardian: _______
- Architect: _______
- Integrator: _______
- Date: _______

## Evidence
- `artifacts/baseline/interaction_matrix.json` (+ optional `INTERACTION_EXCEPTIONS.json`)
- `artifacts/baseline/benchmark_comparisons.json` (≥3 references)
- `data/metadata/physical_constraints.json` applied by integration
- CI logs: Guardian Safety Gate (Phase-2 checks) PASS
