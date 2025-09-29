# Pillar 7: Detection & Measurement Theory

**Scope**  
This pillar links collision-driven dynamics to observable signals by modeling fluorescence detection, sideband spectroscopy, and quantum jump statistics. It derives measurement operators, signal-to-noise ratios, and estimation frameworks for inferring collisions from photonic data.  
The results specify how experiments and numerics should process raw observables to extract temperature, phase, and decoherence metrics.

**Inputs**  
- Open-system dynamics and decoherence channels from [Pillar 6](P6_open_quantum_systems.md)  
- Mode participation data from [Pillars 3](../tier2_system_dynamics/P3_collective_modes.md) and [4](../tier2_system_dynamics/P4_statistical_mechanics.md)  
- Detector characteristics, optical pumping parameters, and laser noise models  

**Outputs**  
- Optical Bloch and rate-equation models producing fluorescence and sideband spectra  
- Mapping from observed counts to motional state estimates and collision detection thresholds  
- Guidelines for experiment/numerics interfaces, including required calibration data  

**Acceptance Criteria**  
- [ ] Derive fluorescence versus temperature curves with uncertainty propagation  
- [ ] Model sideband asymmetry as a function of mode occupations  
- [ ] Quantify detection efficiency and false-positive/negative rates for collision events  
- [ ] Provide calibration routines for detector backgrounds and laser drifts  
- [ ] Update glossary entries for detection efficiencies, branching ratios, and count statistics  

**Validation Script**  
- File: `theory/validation/P7_detection_models.py`  
- Purpose: Simulate fluorescence and sideband signals for benchmark scenarios and compare against analytic predictions  

**Notes & References**  
- See [`_glossary.md`](../_glossary.md) for detection-related symbols and parameters.  
- Reference optical Bloch equation literature and measurement theory texts cited in [`_references.bib`](../_references.bib).  
