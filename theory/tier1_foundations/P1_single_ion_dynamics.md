[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/uwarring82/-flyby-fingerprints-sandbox/HEAD?labpath=theory%2Ftier1_foundations%2Fnotebooks%2FP1_examples_mg_ba.ipynb)

# Pillar 1: Single-Ion Dynamics

**Scope**
This pillar establishes the baseline physics of a single ion confined in a radio-frequency (RF) Paul trap. It covers the Mathieu equation of motion, secular motion, micromotion, and the mapping to the quantum harmonic oscillator. The discussion also sets the Lamb–Dicke regime, zero-point fluctuations, and canonical scaling laws that downstream tracks reuse when benchmarking trap configurations.

> **Worked examples**
> For Mg⁺ and Ba⁺ calculations, plots, and executable parameter sweeps, launch the companion notebook [`P1_examples_mg_ba.ipynb`](notebooks/P1_examples_mg_ba.ipynb).

## Classical description
An ideal linear Paul trap applies a potential of the form
\[
\Phi(x, y, t) = \frac{V_\text{rf}}{2r_0^2}(x^2 - y^2)\cos(\Omega_\text{rf} t) + \frac{U_\text{dc}}{2r_0^2}(x^2 - y^2) + \frac{\kappa U_\text{end}}{z_0^2}\left(z^2 - \frac{x^2 + y^2}{2}\right),
\]
where $V_\text{rf}$ is the drive amplitude at angular frequency $\Omega_\text{rf}$, $r_0$ and $z_0$ are characteristic electrode dimensions, $U_\text{dc}$ is an applied static quadrupole voltage, and $\kappa$ parameterizes geometric efficiency.

The ion motion separates into radial $(x, y)$ and axial $(z)$ coordinates, each satisfying Mathieu-type equations
\[
\frac{\mathrm{d}^2 u}{\mathrm{d}\tau^2} + \left(a_u - 2 q_u \cos 2\tau\right) u = 0,
\]
with $\tau = \Omega_\text{rf} t / 2$ and $u \in \{x, y, z\}$. The stability parameters are
\[
q_{x,y} = \frac{2 Q V_\text{rf}}{m r_0^2 \Omega_\text{rf}^2}, \qquad a_{x,y} = \frac{4 Q U_\text{dc}}{m r_0^2 \Omega_\text{rf}^2} - \frac{2 Q \kappa U_\text{end}}{m z_0^2 \Omega_\text{rf}^2},
\]
\[
q_z = 0, \qquad a_z = \frac{8 Q \kappa U_\text{end}}{m z_0^2 \Omega_\text{rf}^2},
\]
where $Q$ and $m$ denote the ion charge and mass.

Stable confinement requires $(a_u, q_u)$ to lie within the lowest Mathieu stability region. For small $|q_u|$ and $|a_u|$, the secular frequency is
\[
\omega_{u,\text{sec}} \approx \frac{\Omega_\text{rf}}{2} \sqrt{a_u + \frac{1}{2} q_u^2}.
\]

## Micromotion
The total motion comprises slow secular oscillations plus fast micromotion at the RF frequency. The micromotion amplitude $u_\text{mm}$ associated with the intrinsic trap fields is proportional to the secular displacement $u_0$ through
\[
\frac{u_\text{mm}}{u_0} \approx \frac{q_u}{2}
\]
in the pseudopotential limit.

Static stray electric fields $E_\text{dc}$ displace the ion from the RF null, adding excess micromotion with amplitude
\[
u_\text{mm} = \frac{Q E_\text{dc}}{m \Omega_\text{rf}^2}.
\]
The corresponding kinetic energy averaged over an RF cycle is
\[
\langle E_\text{mm} \rangle = \frac{1}{4} m \Omega_\text{rf}^2 u_\text{mm}^2.
\]

Mitigation strategies include DC compensation electrodes, parametric excitation to probe residual micromotion, photon-correlation measurements, and resolved-sideband thermometry of the secular modes.

## Quantum description
Each secular mode is approximated as a quantum harmonic oscillator with Hamiltonian
\[
H = \frac{p^2}{2 m} + \frac{1}{2} m \omega_{u,\text{sec}}^2 u^2.
\]
The ground-state wavefunction width (zero-point motion) is
\[
\Delta u_0 = \sqrt{\frac{\hbar}{2 m \omega_{u,\text{sec}}}}.
\]

The Lamb–Dicke parameter for a laser of wavelength $\lambda$ addressing the mode is
\[
\eta = k \Delta u_0 = \frac{2 \pi}{\lambda} \sqrt{\frac{\hbar}{2 m \omega_{u,\text{sec}}}}.
\]
The Lamb–Dicke regime is characterized by $\eta^2 (2 \bar{n} + 1) \ll 1$, ensuring that motional sidebands are weakly excited.

## Diagnostics and calibration
- **Secular frequency scans:** Apply parametric heating via electrode modulation to map $\omega_{u,\text{sec}}$.
- **Doppler modulation:** Detect micromotion through phase-sensitive fluorescence modulation at $\Omega_\text{rf}$.
- **Resolved sideband spectroscopy:** Measure $\eta$ and motional occupation numbers.
- **Photon correlation / RF correlation:** Infer residual micromotion amplitude via time-correlated photon arrival histograms.

## References
- D. J. Wineland, “Quantum state manipulation of trapped ions,” in *Reviews of Modern Physics* **75**, 2003.
- H. G. Dehmelt, “Radiofrequency spectroscopy of stored ions,” *Advances in Atomic and Molecular Physics* **3**, 1967.
- R. Blatt and D. Wineland, “Entangled states of trapped atomic ions,” *Nature* **453**, 2008.

