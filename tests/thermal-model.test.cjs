"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const model = require("../site/labs/thermal-model.js");

const referenceInput = {
  sigma0Nm: 20,
  projectedRangeNm: 80,
  doseCm2: 2e13,
  backgroundCm3: 1e16,
  holds: [{ tempC: 1050, timeS: 20 }]
};

test("reference case matches independently calculated analytical values", function () {
  const result = model.calculate(referenceInput);
  assert.ok(Math.abs(result.holds[0].diffusivityCm2PerS - 5.03425859324e-14) < 1e-24);
  assert.ok(Math.abs(result.sigmaFinalNm - 24.522853499) < 1e-8);
  assert.ok(Math.abs(result.peakCm3 - 3.2536367e18) < 1e11);
  assert.ok(Math.abs(result.rightCrossingNm - 163.413350077) < 1e-6);
  assert.equal(result.highConcentrationCaution, false);
});

test("high-concentration literature caution has a boundary and regression check", function () {
  const threshold = model.constants.concentrationEffectsCautionCm3;
  const denominator = Math.sqrt(2 * Math.PI) * (100 / 1e7);
  const doseAtThreshold = threshold * denominator;
  const atThreshold = model.calculate({
    sigma0Nm: 100, projectedRangeNm: 0, doseCm2: doseAtThreshold,
    backgroundCm3: 1e16, holds: []
  });
  assert.ok(Math.abs(atThreshold.peakCm3 / threshold - 1) < 1e-14);
  assert.equal(atThreshold.highConcentrationCaution, false);

  const justBelow = model.calculate({
    sigma0Nm: 100, projectedRangeNm: 0, doseCm2: doseAtThreshold * (1 - 1e-9),
    backgroundCm3: 1e16, holds: []
  });
  const justAbove = model.calculate({
    sigma0Nm: 100, projectedRangeNm: 0, doseCm2: doseAtThreshold * (1 + 1e-9),
    backgroundCm3: 1e16, holds: []
  });
  assert.ok(justBelow.peakCm3 < threshold);
  assert.equal(justBelow.highConcentrationCaution, false);
  assert.ok(justAbove.peakCm3 > threshold);
  assert.equal(justAbove.highConcentrationCaution, true);

  const reviewerEdge = model.calculate({
    sigma0Nm: 0.5, projectedRangeNm: 80, doseCm2: 1e15,
    backgroundCm3: 1e16, holds: [{ tempC: 850, timeS: 0.1 }]
  });
  assert.ok(reviewerEdge.peakCm3 > 7.8e21 && reviewerEdge.peakCm3 < 8.1e21);
  assert.equal(reviewerEdge.highConcentrationCaution, true);
});

test("sequential same-law holds add the diffusion integral", function () {
  const split = model.calculate({ ...referenceInput, holds: [
    { tempC: 1050, timeS: 8 }, { tempC: 1050, timeS: 12 }
  ] });
  const single = model.calculate(referenceInput);
  assert.ok(Math.abs(split.sigmaFinalNm - single.sigmaFinalNm) < 1e-12);
});

test("hotter hold has greater Arrhenius diffusivity inside the declared range", function () {
  assert.ok(model.diffusivityCm2PerS(1100) > model.diffusivityCm2PerS(850));
});

test("the thermal model accepts exactly 30 holds and rejects a 31st", function () {
  const maximum = Array.from({ length: 30 }, () => ({ tempC: 900, timeS: 1 }));
  const accepted = model.calculate({ ...referenceInput, holds: maximum });
  assert.equal(accepted.holds.length, 30);
  assert.throws(() => model.calculate({ ...referenceInput, holds: maximum.concat({ tempC: 900, timeS: 1 }) }), /30/);
});

test("profile sampling returns the modeled peak at projected range", function () {
  const result = model.calculate(referenceInput);
  const concentration = model.concentrationAtNm(referenceInput.projectedRangeNm, referenceInput, result);
  assert.ok(Math.abs(concentration / result.peakCm3 - 1) < 1e-14);
});

test("non-crossing profiles report null instead of a complex or misleading depth", function () {
  const result = model.calculate({ ...referenceInput, doseCm2: 1e11, backgroundCm3: 1e19 });
  assert.equal(result.rightCrossingNm, null);
});

test("invalid temperatures, hold duration, and physical inputs fail with clear errors", function () {
  assert.throws(() => model.calculate({ ...referenceInput, holds: [{ tempC: 849, timeS: 10 }] }), /850/);
  assert.throws(() => model.calculate({ ...referenceInput, holds: [{ tempC: 900, timeS: 0 }] }), /duration/);
  assert.throws(() => model.calculate({ ...referenceInput, sigma0Nm: NaN }), /sigma/);
  assert.throws(() => model.calculate({ ...referenceInput, holds: Array(31).fill({ tempC: 900, timeS: 1 }) }), /30/);
});
