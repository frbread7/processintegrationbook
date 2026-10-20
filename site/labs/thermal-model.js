(function (root, factory) {
  "use strict";
  const model = factory();
  if (typeof module === "object" && module.exports) module.exports = model;
  if (root) root.ProcessIntegrationThermalModel = model;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const K_B_EV_PER_K = 8.617333262145e-5;
  const D0_CM2_PER_S = 0.76;
  const EA_EV = 3.46;
  const SQRT_2_PI = Math.sqrt(2 * Math.PI);
  const CM_TO_NM = 1e7;
  // Literature-based warning marker only; it is not a universal physical cutoff.
  const CONCENTRATION_EFFECTS_CAUTION_CM3 = 2e19;

  function requireFinite(name, value, min, max) {
    if (typeof value !== "number" || !Number.isFinite(value) || value < min || value > max) {
      throw new RangeError(name + " must be a finite number in [" + min + ", " + max + "].");
    }
  }

  function diffusivityCm2PerS(tempC) {
    requireFinite("Temperature (°C)", tempC, 850, 1100);
    const tempK = tempC + 273.15;
    return D0_CM2_PER_S * Math.exp(-EA_EV / (K_B_EV_PER_K * tempK));
  }

  function calculate(input) {
    if (!input || typeof input !== "object") throw new TypeError("Provide a model input object.");
    const { sigma0Nm, projectedRangeNm, doseCm2, backgroundCm3, holds } = input;
    requireFinite("Initial sigma (nm)", sigma0Nm, 0.5, 100);
    requireFinite("Projected range (nm)", projectedRangeNm, 0, 500);
    requireFinite("Dose (cm⁻²)", doseCm2, 1e11, 1e15);
    requireFinite("Background concentration (cm⁻³)", backgroundCm3, 1e14, 1e19);
    if (!Array.isArray(holds) || holds.length > 30) {
      throw new TypeError("Holds must be an array containing at most 30 records.");
    }

    let thetaCm2 = 0;
    const holdResults = holds.map(function (hold, index) {
      if (!hold || typeof hold !== "object") throw new TypeError("Hold " + (index + 1) + " must be an object.");
      requireFinite("Hold " + (index + 1) + " temperature (°C)", hold.tempC, 850, 1100);
      requireFinite("Hold " + (index + 1) + " duration (s)", hold.timeS, 0.1, 3600);
      const diffusivity = diffusivityCm2PerS(hold.tempC);
      const exposure = diffusivity * hold.timeS;
      thetaCm2 += exposure;
      return { tempC: hold.tempC, timeS: hold.timeS, diffusivityCm2PerS: diffusivity, exposureCm2: exposure };
    });

    const sigma0Cm = sigma0Nm / CM_TO_NM;
    const sigmaFinalCm = Math.sqrt(sigma0Cm * sigma0Cm + 2 * thetaCm2);
    const sigmaFinalNm = sigmaFinalCm * CM_TO_NM;
    const projectedRangeCm = projectedRangeNm / CM_TO_NM;
    // Reflect the initial Gaussian lobe at x=0 (Neumann/no-flux boundary).
    // Rp is the lobe center, not the mean depth when the surface is nearby.
    const modeCm = foldedMode(projectedRangeCm, sigmaFinalCm);
    const peakCm3 = foldedConcentration(modeCm, projectedRangeCm, sigmaFinalCm, doseCm2);
    let crossingCm = null;
    if (peakCm3 > backgroundCm3) {
      let lo = modeCm;
      let hi = projectedRangeCm + 10 * sigmaFinalCm;
      while (foldedConcentration(hi, projectedRangeCm, sigmaFinalCm, doseCm2) > backgroundCm3) hi = 2 * hi + sigmaFinalCm;
      for (let i = 0; i < 100; i += 1) {
        const mid = (lo + hi) / 2;
        if (foldedConcentration(mid, projectedRangeCm, sigmaFinalCm, doseCm2) > backgroundCm3) lo = mid;
        else hi = mid;
      }
      crossingCm = (lo + hi) / 2;
    }

    return {
      parameters: { d0Cm2PerS: D0_CM2_PER_S, activationEnergyEv: EA_EV, boltzmannEvPerK: K_B_EV_PER_K },
      holds: holdResults,
      thetaCm2: thetaCm2,
      sigmaFinalNm: sigmaFinalNm,
      peakCm3: peakCm3,
      rightCrossingNm: crossingCm === null ? null : crossingCm * CM_TO_NM,
      modeNm: modeCm * CM_TO_NM,
      surfaceBoundaryMatters: projectedRangeNm < 3 * sigmaFinalNm,
      // Backward-compatible name; this now flags where the reflected boundary
      // assumption matters, not literal loss by truncating the profile.
      surfaceTruncationLikely: projectedRangeNm < 3 * sigmaFinalNm,
      reflectingBoundaryIdealization: true,
      highConcentrationCaution: peakCm3 > CONCENTRATION_EFFECTS_CAUTION_CM3
    };
  }

  function concentrationAtNm(xNm, input, result) {
    requireFinite("Depth (nm)", xNm, 0, Number.MAX_VALUE);
    if (!input || !result || !Number.isFinite(result.sigmaFinalNm)) {
      throw new TypeError("Calculate a valid profile before sampling it.");
    }
    const sigmaCm = result.sigmaFinalNm / CM_TO_NM;
    const xCm = xNm / CM_TO_NM;
    const rpCm = input.projectedRangeNm / CM_TO_NM;
    return foldedConcentration(xCm, rpCm, sigmaCm, input.doseCm2);
  }

  function foldedConcentration(xCm, rpCm, sigmaCm, doseCm2) {
    const scale = doseCm2 / (SQRT_2_PI * sigmaCm);
    const a = Math.exp(-Math.pow(xCm - rpCm, 2) / (2 * sigmaCm * sigmaCm));
    const b = Math.exp(-Math.pow(xCm + rpCm, 2) / (2 * sigmaCm * sigmaCm));
    return scale * (a + b);
  }

  function foldedMode(rpCm, sigmaCm) {
    if (rpCm <= sigmaCm) return 0;
    let lo = 0;
    let hi = rpCm;
    for (let i = 0; i < 100; i += 1) {
      const mid = (lo + hi) / 2;
      // Stationary point: x = Rp tanh(x Rp / sigma^2).
      if (rpCm * Math.tanh(mid * rpCm / (sigmaCm * sigmaCm)) > mid) lo = mid;
      else hi = mid;
    }
    return (lo + hi) / 2;
  }

  return Object.freeze({
    constants: Object.freeze({
      kBEvPerK: K_B_EV_PER_K,
      d0Cm2PerS: D0_CM2_PER_S,
      eaEv: EA_EV,
      concentrationEffectsCautionCm3: CONCENTRATION_EFFECTS_CAUTION_CM3
    }),
    diffusivityCm2PerS: diffusivityCm2PerS,
    calculate: calculate,
    concentrationAtNm: concentrationAtNm
  });
});
