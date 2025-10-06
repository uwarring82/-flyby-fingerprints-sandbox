# Fly-by Fingerprints Sandbox

[Wiki Home](https://github.com/uwarring82/-flyby-fingerprints-sandbox/wiki) · [Theory Track](/theory) · [Numerics Track](/numerics) · [Experiments Track](/experiments) · [Status](./STATUS.md)

Ion–neutral collision signatures in trapped-ion systems: a sandbox to develop the theory, numerics, and experimental playbooks needed to detect and interpret fly-by events.

> **Working mode:** Three tracks run in parallel — **Theory (priority 1)**, **Numerics (priority 2)**, **Experiments (priority 3)** — with agile, rolling decisions.

---

## Tracks

### 1) Theory (Priority 1)
- Purpose: Define foundational physics, interactions, and observable mappings.
- Outputs: Pillar docs (P1–P9), acceptance checklists, validation snippets, shared glossary.
- Start here if you’re new.

**Entry point:** [`theory/`](theory/) • Glossary: [`theory/_glossary.md`](theory/_glossary.md)

### 2) Numerics (Priority 2)
- Purpose: Reliable simulation of ion motion, collisions, and decoherence with tested benchmarks.
- Outputs: MD/symplectic integrators, MC collision kernels, convergence tests, CI.

**Entry point:** [`numerics/`](numerics/)

### 3) Experiments (Priority 3)
- Purpose: Practical procedures, calibration, and data-taking templates to validate predictions.
- Outputs: Setup notes, checklists, acquisition scripts, analysis notebooks.

**Entry point:** [`experiments/`](experiments/)

---

## Scaffold: Pillars (titles only)
- **P1** Single-Ion Dynamics  
- **P2** Collision Fundamentals  
- **P3** Collective Modes in Ion Chains  
- **P4** Statistical Mechanics of Collisions  
- **P5** Structural & Plasma Regimes  
- **P6** Open Quantum System Dynamics  
- **P7** Detection & Measurement Theory  
- **P8** Experimental Systematics & Backgrounds  
- **P9** Numerical Methods & Computational Validation

*(Details live in the `theory/` track; numerics/experiments consume those interfaces.)*

---

## Quick Start

```bash
# clone
git clone https://github.com/uwarring82/-flyby-fingerprints-sandbox.git
cd -flyby-fingerprints-sandbox

# set up python env (example)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # if present

# run sample validations (when available)
# python theory/validation/P1_trap_frequencies.py
# python numerics/tests/test_integrators.py
```

---

## Contributing & Reviews
- Branching: `feat/<track>-<short-name>` (e.g., `feat/theory-p2-langevin`).
- PRs: Small, focused; include a checklist line for what was validated.
- Reviews: Guardian checks acceptance items; Architect checks structure; Integrator merges.
- Glossary discipline: Add/modify symbols only in [`theory/_glossary.md`](theory/_glossary.md); link from your doc.
- Docs style: Keep it concise; one file per topic; cross-link instead of duplicating.

---

## Roadmap & Working Agreements
- Parallel tracks with rolling gates; Phase-2 (numerics) may start once Theory drafts provide safe-to-consume interfaces.
- Minimal viable drafts first; refine iteratively.
- Validation first: every new model or kernel ships with a tiny, runnable check.

---

## Documentation & Guides

- **Start in the Wiki:** [Wiki Home](https://github.com/uwarring82/-flyby-fingerprints-sandbox/wiki) · [Guardian Workflows](https://github.com/uwarring82/-flyby-fingerprints-sandbox/wiki/Guardian_Workflows) · [Theory Track](https://github.com/uwarring82/-flyby-fingerprints-sandbox/wiki/Theory_Track) · [Numerics Track](https://github.com/uwarring82/-flyby-fingerprints-sandbox/wiki/Numerics_Track) · [Experiments Track](https://github.com/uwarring82/-flyby-fingerprints-sandbox/wiki/Experiments_Track)

---

## License & Acknowledgements
- License: See [`LICENSE`](LICENSE).
- Contributors: Council-3 (Architect, Guardian, Integrator) and collaborators.

