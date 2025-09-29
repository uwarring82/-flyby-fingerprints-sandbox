# Pillar 2: Collision Fundamentals

**Scope**  
This pillar characterizes binary ion–neutral encounters from classical and quantum perspectives. It develops ion–neutral potentials, Langevin capture rates, and the role of polarization forces, then extends to partial-wave scattering and energy-dependent cross sections.  
The goal is to translate microscopic collision physics into rate coefficients and momentum-transfer kernels that higher-tier pillars reuse.

**Inputs**  
- Trap environment from [Pillar 1](P1_single_ion_dynamics.md): secular frequencies, velocity scales  
- Neutral background properties: species, density, temperature, polarizability  
- Atomic constants and potential parameters sourced from literature  

**Outputs**  
- Langevin capture rates, elastic/inelastic cross sections σ(E), and momentum-transfer coefficients  
- Energy and angular distributions for single-collision events  
- Parameterized collision kernels supplied to statistical and open-system models  

**Acceptance Criteria**  
- [ ] Derive Langevin rate constant and compare with reference data  
- [ ] Compute σ(E) for benchmark neutral species with uncertainty estimates  
- [ ] Document thresholds for inelastic channels relevant to Mg⁺ and Ba⁺  
- [ ] Provide sampling routines for scattering angle distributions  
- [ ] Update glossary entries for σ(E), k_L, and polarization potentials  

**Validation Script**  
- File: `theory/validation/P2_collision_rates.py`  
- Purpose: Evaluate Langevin rates and generate σ(E) curves across relevant energies  

**Notes & References**  
- See [`_glossary.md`](../_glossary.md) for symbols such as σ(E) and k_L.  
- Reference Langevin (1905) and modern collision reviews cited in [`_references.bib`](../_references.bib).  
