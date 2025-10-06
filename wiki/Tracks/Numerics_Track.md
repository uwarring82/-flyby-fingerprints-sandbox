# Numerics Track

## Purpose & Outputs
- [ ] Build molecular dynamics & symplectic integrators aligned with Theory interfaces.
- [ ] Implement Monte Carlo collision kernels and convergence harnesses.
- [ ] Maintain CI hooks for Guardian validation.
- Entry folder: [`numerics/`](../../tree/main/numerics/)

## Interfaces Consumed from Theory
| Interface | Status | Source |
| --- | --- | --- |
| Trap parameter schema (`Ω_rf`, `q`, `a`, `V_rf`, `z₀`, `ω_sec`) | Drafting under review | [`theory/tier1_foundations/P1_single_ion_dynamics.md`](../../blob/main/theory/tier1_foundations/P1_single_ion_dynamics.md) |
| Collision kernels | Draft | [`theory/tier1_foundations/P2_collision_fundamentals.md`](../../blob/main/theory/tier1_foundations/P2_collision_fundamentals.md) |
| Pillar glossary | Stable | [`theory/_glossary.md`](../../blob/main/theory/_glossary.md) |

## Validation Hooks
- [ ] Null tests vs. analytic secular frequencies.
- [ ] Convergence sweeps captured under [`numerics/tests/`](../../tree/main/numerics/tests/).
- [ ] Guardian ROC suites activated once thresholds lock — see [Guardian Workflows](../Guardian_Workflows).

---
Last synchronized with main on 2025-10-06 (commit fe72749). Owner: CODEX.
