# Pillar 5: Structural & Plasma Regimes

**Scope**  
This pillar maps trapped-ion ensembles onto non-neutral plasma frameworks, clarifying when the system behaves like a liquid, solid, or plasma. It introduces Debye screening, Coulomb coupling Γ, and order parameters that signal phase transitions.  
These results provide diagnostic criteria for when collision-driven heating or external perturbations will trigger structural changes relevant to detection.

**Inputs**  
- Mode structure and spacing from [Pillar 3](P3_collective_modes.md)  
- Temperature evolution and diffusion constants from [Pillar 4](P4_statistical_mechanics.md)  
- Trap geometry and density distributions from experimental specifications  

**Outputs**  
- Phase diagrams linking Γ, λ_D, and density to structural regimes  
- Order parameters and signatures for liquid–solid transitions and plasma behavior  
- Threshold criteria for triggering crystal melting or recrystallization  

**Acceptance Criteria**  
- [ ] Compute Γ and λ_D for benchmark trap conditions and background gases  
- [ ] Produce regime maps showing transitions among crystalline, liquid, and plasma states  
- [ ] Quantify impact of collision-driven heating on structural transitions  
- [ ] Provide guidelines for experimental diagnostics of regime changes  
- [ ] Add glossary entries for Γ, λ_D, and relevant order parameters  

**Validation Script**  
- File: `theory/validation/P5_plasma_regimes.py`  
- Purpose: Evaluate Γ and λ_D across parameter scans and overlay regime boundaries  

**Notes & References**  
- Consult [`_glossary.md`](../_glossary.md) for plasma-physics terminology.  
- Reference non-neutral plasma texts and experimental studies listed in [`_references.bib`](../_references.bib).  
