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
    const peakCm3 = doseCm2 / (SQRT_2_PI * sigmaFinalCm);
    const crossingNm = peakCm3 > backgroundCm3
      ? (projectedRangeCm + sigmaFinalCm * Math.sqrt(2 * Math.log(peakCm3 / backgroundCm3))) * CM_TO_NM
      : null;

    return {
      parameters: { d0Cm2PerS: D0_CM2_PER_S, activationEnergyEv: EA_EV, boltzmannEvPerK: K_B_EV_PER_K },
      holds: holdResults,
      thetaCm2: thetaCm2,
      sigmaFinalNm: sigmaFinalNm,
      peakCm3: peakCm3,
      rightCrossingNm: crossingNm,
      surfaceTruncationLikely: projectedRangeNm < 3 * sigmaFinalNm,
      highConcentrationCaution: peakCm3 > CONCENTRATION_EFFECTS_CAUTION_CM3
    };
  }

  function concentrationAtNm(xNm, input, result) {
    requireFinite("Depth (nm)", xNm, 0, 10000);
    if (!input || !result || !Number.isFinite(result.sigmaFinalNm)) {
      throw new TypeError("Calculate a valid profile before sampling it.");
    }
    const sigmaCm = result.sigmaFinalNm / CM_TO_NM;
    const xCm = xNm / CM_TO_NM;
    const rpCm = input.projectedRangeNm / CM_TO_NM;
    const q = input.doseCm2;
    return q / (SQRT_2_PI * sigmaCm) * Math.exp(-Math.pow(xCm - rpCm, 2) / (2 * sigmaCm * sigmaCm));
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
