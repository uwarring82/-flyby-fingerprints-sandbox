# Pillar 1: Single-Ion Dynamics

**Scope**  
This pillar establishes the baseline physics of a single ion confined in a radio-frequency (RF) Paul trap. It covers the Mathieu equation of motion, secular motion, micromotion, and the mapping to the quantum harmonic oscillator.  
The discussion also sets the Lamb–Dicke regime, zero-point fluctuations, and canonical scaling laws that downstream tracks reuse when benchmarking trap configurations.

**Inputs**  
- Trap parameters: RF drive frequency Ω, voltage V, characteristic electrode dimension r₀  
- Ion species: mass m, charge e, and polarizability α  
- Reference experimental context: Mg⁺ and Ba⁺ benchmark systems  

**Outputs**  
- Secular frequencies (ω_sec), micromotion amplitude β, and stability parameters (q, a)  
- Ground-state spread x₀ and Lamb–Dicke parameters for reference species  
- Tabulated canonical scales for energy, length, and time used across the project  

**Acceptance Criteria**  
- [ ] Derive secular frequency ω_sec for Mg⁺ and Ba⁺ at reference trap parameters  
- [ ] Verify dimensional consistency and stability boundaries of Mathieu q, a parameters  
- [ ] Plot a representative stability diagram highlighting operating points  
- [ ] Compute ground-state spread x₀ and Lamb–Dicke η for both benchmark ions  
- [ ] Register glossary entries for q, a, ω_sec, β, x₀, and η  

**Validation Script**  
- File: `theory/validation/P1_trap_frequencies.py`  
- Purpose: Calculate ω_sec, β, and generate the stability diagram for reference traps  

**Notes & References**  
- See [`_glossary.md`](../_glossary.md) for symbol definitions shared across pillars.  
- Cite Wineland *et al.* and related trap design references listed in [`_references.bib`](../_references.bib).  
