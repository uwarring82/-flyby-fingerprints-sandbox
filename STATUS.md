# Project Status — Flyby Fingerprints

**Last updated:** 2025-09-25

## Phase 1 — Simulation Backend (ACTIVE, Owner: @uwarring82)

**Objective:** Certified background-first simulation stack for trapped-ion heating/“fly-by” fingerprints.

### Modules

- **Physics Engine** — *In Review* (~60%)  
  - **Owner:** @uwarring82  
  - **Focus:** Coulomb precision sweep, time-step/adaptive integrator selection  
  - **Target:** <0.1% deviation vs. analytics; performance guardrails

- **Background Effects** — *Active* (~50%)  
  - **Owner:** @uwarring82  
  - **Implemented:** thermal motion (proxy), EM pickup (mains+broadband), surface drift (random-walk proxy), detection Poisson noise  
  - **Planned next:** PSD checks for RF pickup; Allan-like drift metric; parameter calibration presets  
  - **Notebook:** `notebooks/Background_Model_Explorer.ipynb` (Binder)

- **Collision Injection** — *Pending* (~15%)  
  - **Owner:** @uwarring82  
  - **Planned:** I/O schema with ground-truth labels; `examples/run_collision_injection.py`; baseline tests (null vs. injected)

- **Validation Framework** — *In Review* (~40%)  
  - **Owner:** @uwarring82  
  - **Implemented:** inventory check, null hypothesis (p≥0.05), SNR≥10 gate, contribution stubs  
  - **Planned next:** ROC/AUC harness; CI promotion; baseline artifacts

### Guardian Gates (Phase-1 Exit)
- Background inventory complete (thermal, EM, surface, detection)  
- Null control datasets pass p≥0.05 (Poisson GOF)  
- Claimed signatures satisfy SNR≥10 (sim suites)  
- Physics deviation <0.1% on analytic tasks  
- I/O preserves ground-truth metadata

## Phase 2 — Algorithm Development (GATED)
- A-D-M triad pipeline; ROC suites; detector robustness to systematics

## Phase 3 — Real Data Analysis (GATED)
- Historical re-analysis; new campaigns; community portal

## History / Provenance
- 2025-09-24: Dashboard introduced in README (initial owners/placeholders)  
- 2025-09-25: Owners unified to @uwarring82; Background Explorer + Binder highlighted
