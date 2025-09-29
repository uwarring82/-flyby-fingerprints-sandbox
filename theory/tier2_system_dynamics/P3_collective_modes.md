# Pillar 3: Collective Modes in Ion Chains

**Scope**  
This pillar studies the normal-mode structure of ion chains and Coulomb crystals under realistic trap conditions. It extends single-ion dynamics to many-body configurations, analyzing axial and radial spectra, mode couplings, and structural transitions such as zig-zag instabilities.  
Results set the mechanical eigenbasis required to describe heating, cooling, and detection channels in subsequent pillars.

**Inputs**  
- Single-ion frequencies and scaling laws from [Pillar 1](../tier1_foundations/P1_single_ion_dynamics.md)  
- Inter-ion spacing, crystal geometry, and ion number  
- Trap anisotropy parameters and boundary conditions  

**Outputs**  
- Mode matrices, eigenfrequencies, and participation factors for axial/radial branches  
- Stability thresholds for structural transitions across parameter sweeps  
- Reduced models for mode-resolved coupling to collisions and detection schemes  

**Acceptance Criteria**  
- [ ] Compute mode spectra for linear chains of 2–50 ions with convergence tests  
- [ ] Identify zig-zag transition points as functions of trap anisotropy  
- [ ] Provide mode participation tables consumable by numerics and detection models  
- [ ] Quantify sensitivity of key modes to stray fields and micromotion  
- [ ] Add glossary entries for normal-mode indices and participation factors  

**Validation Script**  
- File: `theory/validation/P3_mode_spectra.py`  
- Purpose: Generate axial and radial mode spectra, verifying transition thresholds  

**Notes & References**  
- Consult [`_glossary.md`](../_glossary.md) for mode-labeling conventions.  
- Cite non-neutral plasma and trapped-ion normal-mode references listed in [`_references.bib`](../_references.bib).  
