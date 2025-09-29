# Theory Track

The **Theory Track** defines the physics baseline for the Fly-by Fingerprints project.  
It provides modular descriptions of ion dynamics, collisions, statistical mechanics, and detection theory.  
All downstream tracks (Numerics, Experiments) depend on these definitions.  

> **Priority:** Theory comes first. Numerics and Experiments only start once minimal viable theory pillars are in place.  
> **Outputs:** Pillar docs (`P*.md`), validation scripts (`validation/`), glossary (`_glossary.md`), and references (`_references.bib`).  

---

## Structure

The theory is organized into **three tiers** and nine **pillars**:

### Tier 1 – Foundational Primitives
- [P1 — Single-Ion Dynamics](tier1_foundations/P1_single_ion_dynamics.md)  
  *Trap Hamiltonian, secular motion, micromotion, harmonic oscillator, Lamb–Dicke regime. Provides canonical scales (ω_sec, q, a, x₀).*  

- [P2 — Collision Fundamentals](tier1_foundations/P2_collision_fundamentals.md)  
  *Ion–neutral potentials, Langevin capture, quantum scattering. Defines cross-sections and single-event transfer rates.*  

### Tier 2 – System-Level & Statistical Dynamics
- [P3 — Collective Modes in Ion Chains](tier2_system_dynamics/P3_collective_modes.md)  
  *Normal modes of chains/crystals, axial and radial spectra, zig-zag transitions. Provides basis for mode-resolved heating.*  

- [P4 — Statistical Mechanics of Collisions](tier2_system_dynamics/P4_statistical_mechanics.md)  
  *From single collisions to ensemble heating/cooling. Rate equations and diffusion models yielding T(t) and heating rates.*  

- [P5 — Structural & Plasma Regimes](tier2_system_dynamics/P5_structural_plasma.md)  
  *Non-neutral plasma language: Debye length, Γ, liquid–solid transitions. Connects density/temperature to order parameters and phase-change signatures.*  

### Tier 3 – Observational & Implementation Framework
- [P6 — Open Quantum System Dynamics](tier3_framework/P6_open_quantum_systems.md)  
  *Master equations, Lindblad terms, quantum trajectories. Outputs coherence times and decoherence channels from collisions.*  

- [P7 — Detection & Measurement Theory](tier3_framework/P7_detection_theory.md)  
  *Optical Bloch equations, fluorescence thermometry, sidebands, quantum jumps. Connects collisions and phase transitions to observables.*  

- [P8 — Experimental Systematics & Backgrounds](tier3_framework/P8_systematics_backgrounds.md)  
  *Catalog of technical noise (E-field, B-field, laser, detectors). Provides budgets and calibration protocols.*  

- [P9 — Numerical Methods & Computational Validation](tier3_framework/P9_numerical_methods.md)  
  *Simulation algorithms (MD, symplectic, MC collisions), convergence tests, benchmarks. Ensures reliability of numerics.*  

---

## Supporting Material

- [`_glossary.md`](./_glossary.md): central definitions of symbols and parameters.  
- [`_references.bib`](./_references.bib): canonical references and citations.  
- [`validation/`](./validation/): scripts for quick, canonical checks of pillar results.  

---

## Contribution Guide

- Draft → Minimal viable version → Guardian review → Approved.  
- Always update the glossary when introducing symbols.  
- Cite peer-reviewed sources via `_references.bib`.  
- Add a validation script when introducing new derivations.  
