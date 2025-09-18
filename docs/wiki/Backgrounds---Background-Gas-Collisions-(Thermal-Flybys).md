SPDX-License-Identifier: GPL-3.0-or-later

# Background-Gas Collisions (“Thermal Flybys”)

**What it is.** Collisions with residual-gas molecules cause **impulsive momentum kicks** and non-Gaussian energy tails.

## Rates & signatures
- **Langevin rate** (ion–induced dipole capture) sets a pressure-proportional collision rate \(k_L\) nearly independent of energy in the thermal regime.
- **Statistical fingerprints:** Power-law energy/velocity tails and burstiness; mass-ratio dependent exponents.

## Diagnostics we will run
- **Pressure scans** (controlled leak or RGA-guided) to test linearity of event/heating rate vs pressure.
- **Temporal clustering tests** (runs/over-dispersion; Ljung–Box; Allan variance).
- **Mass dependence** when a dominant background species can be changed (e.g., He vs N\(_2\)).

## Mitigations / controls
- Improve base pressure; reduce outgassing; bake; cryo-pumping surfaces.
- Shield from pressure spikes (valve operations, gas loads).

## Primary references
- DeVoe, **Phys. Rev. Lett. 102, 063001 (2009)** (power-law tails). DOI: 10.1103/PhysRevLett.102.063001  
- Grier et al., **Phys. Rev. Lett. 102, 223201 (2009)** (Langevin regime in hybrid setups). DOI: 10.1103/PhysRevLett.102.223201  
- Tomza et al., **Rev. Mod. Phys. 91, 035001 (2019)** (hybrid ion–atom review incl. Langevin). DOI: 10.1103/RevModPhys.91.035001  
- Wineland et al., NIST notes (background gas heating discussion).  
- Major, Gheorghe, Werth, *Charged Particle Traps* (Springer, 2005).
