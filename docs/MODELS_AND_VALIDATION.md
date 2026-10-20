# Models and validation status

## Thermal-history and Gaussian profile experiment

**Status:** Analytically derived and independently numerically cross-checked · model-limited. The half-line solution is supported by an accessible PDE reference, but the selected implant boundary and coefficients are not calibrated against a manufacturing process or validated against real silicon.

### Model

For each constant-temperature hold i, use a conventional dilute boron-in-silicon Arrhenius parameterization. Esser, Hobart, and Kub print the selected prefactor and activation energy in their 2004 calculation (p. G387) and cite S. M. Sze's edited *VLSI Technology* (1983). Mostafa and Medraj's 2017 review also prints the intrinsic-diffusivity equation and cites W. J. Scotten's *Diffusion in Silicon* (2000). Neither historical source's original page/table was independently verified, so the original provenance remains unresolved. The model uses the values reported by these accessible publications as an illustrative historical starting point; the pair is not universal or calibrated for a process:

~~~text
D(Tᵢ) = D₀ exp(−Eₐ / (kB Tᵢ))
Θ = Σᵢ D(Tᵢ) tᵢ
~~~

For a one-dimensional silicon half-space `x ≥ 0`, take `Q` to be the initial chemical dopant dose *within silicon*, `Rp` to be the center of each Gaussian image lobe, and a reflecting no-flux surface at `x = 0`. The initial profile is a pair of positive images with component width `σ₀`. Under Fick's second law with spatially uniform, concentration-independent diffusivity, each component broadens to `σf`:

~~~text
σf² = σ₀² + 2Θ
C(x) = Q / (√(2π) σf) · {exp[−(x − Rp)² / (2σf²)] + exp[−(x + Rp)² / (2σf²)]}, x ≥ 0
∂C/∂x at x=0 = 0; ∫₀∞ C(x) dx = Q; C(x) → 0 as x → ∞
~~~

The image derivatives cancel at the surface, and the two half-line integrals sum to `Q`. The component width `σf` is generally **not** the standard deviation of the normalized half-line profile, and `Rp` is generally **not** its mean depth near the surface. The peak may be at `x=0` or at a positive mode. For `Rp>σf`, the positive mode solves `xmode = Rp tanh(xmode Rp / σf²)`; otherwise the mode is at the surface. If the peak concentration exceeds the uniform opposite-type background `NB`, the lab numerically solves the *descending right-side* crossing `C(x*)=NB` by bracketing and bisection. No crossing is reported when `Cpeak≤NB`. A left-side crossing can also exist and is intentionally omitted. The single-Gaussian closed form does not apply to the image pair.

This is a mathematical Neumann image construction, not a measured implant profile or a physical assertion that a real silicon surface never exchanges or segregates dopant. The equation and boundary construction are mapped to the exact accessible sources in [RECONSTRUCTION_CLAIM_REGISTER.md](RECONSTRUCTION_CLAIM_REGISTER.md) PI-R03–R06.

### Units and inputs

- D₀ = 0.76 cm²/s; Eₐ = 3.46 eV; kB = 8.617333262145 × 10⁻⁵ eV/K. Esser et al. state D₀ and Eₐ but do not spell out D₀'s units in that sentence; the diffusivity prefactor has units cm²/s in the Arrhenius equation, which Mostafa and Medraj explicitly print.
- Temperature is entered in °C from 850 through 1100 °C and converted to kelvin before evaluation.
- Each hold duration is in seconds, from 0.1 through 3600; up to 30 holds may be entered.
- Initial Gaussian-component standard deviation σ₀ and image-lobe center Rp are entered in nm; near the surface these are not generally the width and mean of the normalized silicon-only distribution.
- Implant areal dose Q is in cm⁻²; background concentration NB is in cm⁻³.
- Internal lengths are converted with 1 cm = 10⁷ nm. Θ has cm², and σf has cm before reporting in nm.
- Supported UI ranges are 0.5 ≤ σ₀ ≤ 100 nm, 0 ≤ Rp ≤ 500 nm, 10¹¹ ≤ Q ≤ 10¹⁵ cm⁻², and 10¹⁴ ≤ NB ≤ 10¹⁹ cm⁻³.

Inputs other than the cited Arrhenius parameterization are explicitly synthetic. Zero thermal holds leave the initial profile unchanged; the interface starts with one example hold and can remove it. If `Rp < 3σf`, the UI warns that the idealized reflecting surface matters more; the reflected model still conserves `Q`, so this is not a missing-dose/truncation warning. If `Cpeak≤NB`, the model returns no descending right-side crossing. Fair (1975) reports concentration-dependent profiles for high-concentration boron diffusions above about 2 × 10¹⁹ cm⁻³ in neutral ambients. The UI uses a modeled peak above this approximate value as a literature-informed caution trigger only; the synthetic scenario does not establish Fair's ambient or experimental conditions. It is not a universal physical cutoff or sharp transition, and the calculation still uses the same concentration-independent dilute Arrhenius diffusivity above and below it.

### Assumptions and limits

The model treats each hold as a homogeneous, one-dimensional region with the same dopant and diffusivity law. It starts from the reflected Gaussian chemical dopant distribution, enforces the zero-gradient surface boundary, and compares the profile to a separate uniform background; it does not solve for electrically active carriers or depletion. Temperature ramps are absent; approximating a ramp with holds requires a sufficiently resolved and accurate temperature history.

It omits implant damage and transient-enhanced diffusion, concentration- and charge-state-dependent transport, dopant activation and clustering, oxidation-driven point-defect injection, segregation and moving interfaces, *real* surface exchange/chemistry beyond its fixed no-flux boundary, lateral geometry, strain, and any process-specific calibration. The selected parameter pair is not universal. Fair (1975) reports the concentration-dependent profile behavior in its specific high-concentration neutral-ambient context; Bracht et al. (2007) report dopant diffusion experiments and native-point-defect modeling, and Sadigh et al. (1999) analyze an interstitialcy mechanism atomistically. These sources motivate model limits but do not validate this implementation or calibrate its outputs. The approximate 2 × 10¹⁹ cm⁻³ UI warning marker is literature-informed and deliberately heuristic; it must not be used as a process limit or as evidence that the dilute model is valid below it.

### Analytical reference case

For one 1050 °C, 20 s hold with synthetic σ₀ = 20 nm, Rp = 80 nm, Q = 2 × 10¹³ cm⁻², and NB = 10¹⁶ cm⁻³, the displayed equations give:

- D = 5.03425859324 × 10⁻¹⁴ cm²/s
- σf = 24.522853499 nm
- Cpeak ≈ 3.2536367 × 10¹⁸ cm⁻³ (the peak of the full reflected profile, not one lobe)
- descending right-side x* = 163.413350077 nm

These values are reproduced by browser implementation tests and a separate Python implementation that imports none of the JavaScript code. Independent quadrature checks the `Q` integral after nm-to-cm conversion; boundary-gradient, mode-transition, root residual, deep crossing, narrow-peak sampling, zero-hold, no-crossing, and invalid input/range checks cover distinct properties. This is an analytical and numerical sanity check only. It does not establish a silicon process model.

### Qualitative activities

The process dependency explorer displays declared interface relationships to help learners ask what evidence an integration decision needs. It is not a physical process model or recipe checker. The integration evidence challenge uses a fictional scenario and ordinal feedback; it assigns no probabilities, scores, yield loss, or root cause.
