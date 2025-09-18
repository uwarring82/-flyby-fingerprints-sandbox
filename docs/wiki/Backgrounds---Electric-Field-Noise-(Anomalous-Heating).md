SPDX-License-Identifier: GPL-3.0-or-later

# Electric-Field Noise (“Anomalous Heating”)

**What it is.** Electric-field fluctuations at the ion position that drive motional excitation beyond Johnson noise expectations; commonly associated with surface effects on electrodes.

## Key scalings & equations
- Heating rate for mode of frequency \( \omega \):
  \[
  \dot{\bar n} = \frac{q^2}{4 m \hbar \omega} S_E(\omega)
  \]
  where \(S_E(\omega)\) is the one-sided electric-field noise spectral density.  
- Typical **frequency** scaling: \(S_E(\omega) \propto \omega^{-\beta}\) with \(\beta \sim 1\) (varies by trap and treatment).
- Typical **distance** scaling: \(S_E \propto d^{-\alpha}\), with reports near \(\alpha \approx 3\!-\!4\) in surface traps.
- **Temperature** dependence: rapid increase with temperature; cryo operation strongly suppresses noise in many systems.

## Diagnostics we will run
- **Frequency sweep** of \(\dot{\bar n}(\omega)\) to fit \(\beta\).
- **Distance sweep** in multizone trap (if available) to fit \(\alpha\).
- **Temperature dependence** (if cryo) to extract \(T^\gamma\).
- **Surface treatment tests** (Ar\(^+\) cleaning, laser cleaning) with before/after baselines.

## Mitigations / controls
- Argon-ion in-situ cleaning; pulsed-laser cleaning (355 nm) where compatible.
- Cryogenic operation.
- Strict surface handling / UHV cleanliness.

## Primary references
- Brownnutt, Kumph, Rabl, Blatt, **Rev. Mod. Phys. 87, 1419 (2015)**. DOI: 10.1103/RevModPhys.87.1419  
- Turchette et al., **Phys. Rev. A 61, 063418 (2000)**. DOI: 10.1103/PhysRevA.61.063418  
- Labaziewicz et al., **Phys. Rev. Lett. 101, 180602 (2008)**. DOI: 10.1103/PhysRevLett.101.180602  
- Hite et al., **Phys. Rev. Lett. 109, 103001 (2012)**. DOI: 10.1103/PhysRevLett.109.103001  
- Allcock et al., **New J. Phys. 13, 123023 (2011)**. DOI: 10.1088/1367-2630/13/12/123023  
- Daniilidis et al., **Phys. Rev. B 89, 245435 (2014)**. DOI: 10.1103/PhysRevB.89.245435  
- Sedlacek et al., **Phys. Rev. A 97, 020302 (2018)**. DOI: 10.1103/PhysRevA.97.020302
