# Models and validation status

## Thermal-history and Gaussian profile experiment

**Status:** Analytically checked · model-limited. It is not externally reference-checked as an implementation, calibrated against a manufacturing process, or validated against real silicon.

### Model

For each constant-temperature hold i, use a conventional dilute boron-in-silicon Arrhenius parameterization:

~~~text
D(Tᵢ) = D₀ exp(−Eₐ / (kB Tᵢ))
Θ = Σᵢ D(Tᵢ) tᵢ
~~~

For a one-dimensional, initially Gaussian chemical concentration profile under Fick's second law with spatially uniform, concentration-independent diffusivity:

~~~text
σf² = σ₀² + 2Θ
C(x) = Q / (√(2π) σf) exp[−(x − Rp)² / (2σf²)]
~~~

If the peak concentration is greater than a uniform opposite-type background NB, the positive-depth crossing of this chemical concentration profile is:

~~~text
x* = Rp + σf √(2 ln(Cpeak / NB)), where Cpeak = Q / (√(2π) σf).
~~~

### Units and inputs

- D₀ = 0.76 cm²/s; Eₐ = 3.46 eV; kB = 8.617333262145 × 10⁻⁵ eV/K.
- Temperature is entered in °C from 850 through 1100 °C and converted to kelvin before evaluation.
- Each hold duration is in seconds, from 0.1 through 3600; up to 30 holds may be entered.
- Initial standard deviation σ₀ and projected range Rp are entered in nm.
- Implant areal dose Q is in cm⁻²; background concentration NB is in cm⁻³.
- Internal lengths are converted with 1 cm = 10⁷ nm. Θ has cm², and σf has cm before reporting in nm.
- Supported UI ranges are 0.5 ≤ σ₀ ≤ 100 nm, 0 ≤ Rp ≤ 500 nm, 10¹¹ ≤ Q ≤ 10¹⁵ cm⁻², and 10¹⁴ ≤ NB ≤ 10¹⁹ cm⁻³.

Inputs other than the cited Arrhenius parameterization are explicitly synthetic. If Rp < 3σf, the UI warns that surface truncation may matter. If Cpeak ≤ NB, the model returns no right-side crossing instead of fabricating a value.

### Assumptions and limits

The model treats each hold as a homogeneous, one-dimensional region with the same dopant and diffusivity law. It starts from a Gaussian chemical dopant distribution and compares that profile to a uniform background; it does not solve for electrically active carriers or depletion. Temperature ramps are absent; approximating a ramp with holds requires a sufficiently resolved and accurate temperature history.

It omits implant damage and transient-enhanced diffusion, concentration- and charge-state-dependent transport, dopant activation and clustering, oxidation-driven point-defect injection, segregation and moving interfaces, surface boundary conditions, lateral geometry, strain, and any process-specific calibration. The selected parameter pair is not universal. Fair's model and later experimental/mechanism studies document the concentration, background, ambient, and point-defect dependence that motivates these limits.

### Analytical reference case

For one 1050 °C, 20 s hold with synthetic σ₀ = 20 nm, Rp = 80 nm, Q = 2 × 10¹³ cm⁻², and NB = 10¹⁶ cm⁻³, the displayed equations give:

- D = 5.03425859324 × 10⁻¹⁴ cm²/s
- σf = 24.522853499 nm
- Cpeak ≈ 3.2536367 × 10¹⁸ cm⁻³
- x* = 163.413350077 nm

These values are reproduced by the browser implementation tests and by a separate Python implementation that imports none of the JavaScript code. Tests also check equal-temperature hold additivity, monotonic Arrhenius ordering, peak sampling, no-crossing behavior, and invalid input/range handling. This is a cross-implementation analytical sanity check only.

### Qualitative activities

The process dependency explorer displays declared interface relationships to help learners ask what evidence an integration decision needs. It is not a physical process model or recipe checker. The integration evidence challenge uses a fictional scenario and ordinal feedback; it assigns no probabilities, scores, yield loss, or root cause.
