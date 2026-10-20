(function () {
  "use strict";

  const root = document.documentElement;
  const themeButton = document.querySelector("[data-theme-toggle]");
  const storedTheme = (() => { try { return localStorage.getItem("pib-theme"); } catch (_) { return null; } })();
  if (storedTheme === "dark" || storedTheme === "light") root.dataset.theme = storedTheme;
  if (themeButton) {
    const label = themeButton.querySelector("[data-theme-label]");
    const updateThemeLabel = function () {
      if (label) label.textContent = root.dataset.theme === "dark" ? themeButton.dataset.lightLabel : themeButton.dataset.darkLabel;
    };
    updateThemeLabel();
    themeButton.addEventListener("click", function () {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("pib-theme", next); } catch (_) {}
      updateThemeLabel();
    });
  }

  const menuButton = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector(".main-nav");
  if (menuButton && menu) {
    menuButton.addEventListener("click", function () {
      const open = menu.dataset.open !== "true";
      menu.dataset.open = String(open);
      menuButton.setAttribute("aria-expanded", String(open));
    });
  }

  const search = document.querySelector("[data-chapter-search]");
  if (search) {
    const cards = Array.from(document.querySelectorAll("[data-chapter-card]"));
    const empty = document.querySelector("[data-empty-search]");
    search.addEventListener("input", function () {
      const query = search.value.trim().toLocaleLowerCase();
      let visible = 0;
      cards.forEach(function (card) {
        const show = card.dataset.search.toLocaleLowerCase().includes(query);
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (empty) empty.hidden = visible !== 0;
    });
  }

  document.querySelectorAll("[data-quiz]").forEach(function (quiz) {
    const choices = Array.from(quiz.querySelectorAll("button[data-correct]"));
    let feedback = quiz.querySelector(".quiz-feedback");
    if (!feedback) {
      feedback = document.createElement("p");
      feedback.className = "quiz-feedback";
      feedback.setAttribute("aria-live", "polite");
      quiz.appendChild(feedback);
    }
    choices.forEach(function (choice) {
      choice.setAttribute("aria-pressed", "false");
      choice.addEventListener("click", function () {
        choices.forEach(function (item) { item.setAttribute("aria-pressed", "false"); });
        choice.setAttribute("aria-pressed", "true");
        const isCorrect = choice.dataset.correct === "true";
        feedback.textContent = isCorrect ? quiz.dataset.correctMessage : quiz.dataset.incorrectMessage;
        const explanation = quiz.querySelector(".quiz-explanation");
        if (explanation) explanation.hidden = false;
      });
    });
  });

  const labRoot = document.querySelector("[data-thermal-lab]");
  if (labRoot && window.ProcessIntegrationThermalModel) initThermalLab(labRoot, window.ProcessIntegrationThermalModel);
  initDependencyExplorer();
  initEvidenceChallenge();

  function initThermalLab(rootEl, model) {
    const holdList = rootEl.querySelector("[data-hold-list]");
    const output = rootEl.querySelector("[data-thermal-output]");
    const chart = rootEl.querySelector("[data-profile-chart]");
    const status = rootEl.querySelector("[data-thermal-status]");
    const addButton = rootEl.querySelector("[data-add-hold]");
    const defaults = {
      sigma0Nm: 20, projectedRangeNm: 80, doseCm2: 2e13, backgroundCm3: 1e16,
      holds: [{ tempC: 1050, timeS: 20 }]
    };
    let serial = 0;

    function updateHoldLimit() {
      addButton.disabled = holdList.children.length >= 30;
    }

    function makeHold(hold) {
      if (holdList.children.length >= 30) return;
      serial += 1;
      const row = document.createElement("div");
      row.className = "hold-row";
      row.innerHTML =
        '<div class="field"><label for="hold-temp-' + serial + '">' + rootEl.dataset.tempLabel + '</label>' +
        '<input id="hold-temp-' + serial + '" type="number" min="850" max="1100" step="1" value="' + hold.tempC + '" data-hold-temp></div>' +
        '<div class="field"><label for="hold-time-' + serial + '">' + rootEl.dataset.timeLabel + '</label>' +
        '<input id="hold-time-' + serial + '" type="number" min="0.1" max="3600" step="0.1" value="' + hold.timeS + '" data-hold-time></div>' +
        '<button type="button" data-remove-hold>' + rootEl.dataset.removeLabel + '</button>';
      row.querySelectorAll("input").forEach(function (field) { field.addEventListener("input", calculate); });
      row.querySelector("[data-remove-hold]").addEventListener("click", function () {
        row.remove();
        updateHoldLimit();
        calculate();
      });
      holdList.appendChild(row);
      updateHoldLimit();
    }

    function currentInput() {
      const fields = {};
      rootEl.querySelectorAll("[data-profile-input]").forEach(function (field) {
        fields[field.dataset.profileInput] = field.value.trim() === "" ? NaN : Number(field.value);
      });
      fields.holds = Array.from(holdList.querySelectorAll(".hold-row")).map(function (row) {
        return {
          tempC: row.querySelector("[data-hold-temp]").value.trim() === "" ? NaN : Number(row.querySelector("[data-hold-temp]").value),
          timeS: row.querySelector("[data-hold-time]").value.trim() === "" ? NaN : Number(row.querySelector("[data-hold-time]").value)
        };
      });
      return fields;
    }

    function calculate() {
      try {
        const input = currentInput();
        const result = model.calculate(input);
        output.innerHTML =
          resultItem(rootEl.dataset.sigmaLabel, result.sigmaFinalNm.toFixed(3) + " nm") +
          resultItem(rootEl.dataset.peakLabel, formatScientific(result.peakCm3) + " cm⁻³") +
          resultItem(rootEl.dataset.crossingLabel, result.rightCrossingNm === null ? rootEl.dataset.noCrossingLabel : result.rightCrossingNm.toFixed(3) + " nm");
        const notices = [];
        if (result.surfaceTruncationLikely) notices.push(rootEl.dataset.surfaceWarning);
        if (result.highConcentrationCaution) notices.push(rootEl.dataset.concentrationWarning);
        status.textContent = [rootEl.dataset.modelStatus].concat(notices).join(" ");
        const chartDescription = result.rightCrossingNm === null ? rootEl.dataset.noCrossingChartLabel : rootEl.dataset.backgroundLabel;
        chart.closest("figure").querySelector("figcaption").textContent = chartDescription;
        drawChart(chart, input, result, model, rootEl.dataset.chartXLabel, rootEl.dataset.chartYLabel, chartDescription);
      } catch (error) {
        output.textContent = rootEl.dataset.invalidResult;
        status.textContent = document.documentElement.lang === "ko" ? rootEl.dataset.invalidResult : error.message;
        chart.replaceChildren();
        chart.closest("figure").querySelector("figcaption").textContent = rootEl.dataset.invalidResult;
      }
    }

    function reset() {
      rootEl.querySelectorAll("[data-profile-input]").forEach(function (field) {
        field.value = defaults[field.dataset.profileInput];
      });
      holdList.replaceChildren();
      defaults.holds.forEach(makeHold);
      calculate();
    }

    rootEl.querySelectorAll("[data-profile-input]").forEach(function (field) { field.addEventListener("input", calculate); });
    addButton.addEventListener("click", function () {
      if (holdList.children.length >= 30) return;
      makeHold({ tempC: 950, timeS: 10 });
      calculate();
    });
    rootEl.querySelector("[data-reset-thermal]").addEventListener("click", reset);
    defaults.holds.forEach(makeHold);
    calculate();
  }

  function resultItem(label, value) {
    const box = document.createElement("div");
    box.className = "result-item";
    const name = document.createElement("span");
    name.textContent = label;
    const result = document.createElement("strong");
    result.textContent = value;
    box.append(name, result);
    return box.outerHTML;
  }

  function formatScientific(value) {
    return value.toExponential(3).replace("e+", " × 10^").replace("e-", " × 10^-");
  }

  function drawChart(svg, input, result, model, xLabel, yLabel, backgroundLabel) {
    const width = 720;
    const height = 260;
    const left = 60;
    const right = 18;
    const top = 18;
    const bottom = 43;
    const plotWidth = width - left - right;
    const plotHeight = height - top - bottom;
    const sigma = result.sigmaFinalNm;
    const maxX = result.rightCrossingNm === null
      ? Math.max(220, input.projectedRangeNm + 5 * sigma)
      : Math.max(220, input.projectedRangeNm + 5 * sigma, result.rightCrossingNm * 1.15);
    const sampleXs = new Set();
    for (let i = 0; i <= 120; i += 1) sampleXs.add(maxX * i / 120);
    [0.25, 0.5, 1, 2].forEach(function (multiple) {
      const offset = multiple * sigma;
      [result.modeNm - offset, result.modeNm + offset].forEach(function (x) {
        if (x >= 0 && x <= maxX) sampleXs.add(x);
      });
    });
    [result.modeNm, result.rightCrossingNm].forEach(function (x) {
      if (x !== null && x >= 0 && x <= maxX) sampleXs.add(x);
    });
    const sortedXs = Array.from(sampleXs).sort(function (a, b) { return a - b; });
    const points = [];
    sortedXs.forEach(function (x, index) {
      const c = model.concentrationAtNm(x, input, result);
      const normalized = Math.min(1, c / result.peakCm3);
      const px = left + plotWidth * x / maxX;
      const py = top + plotHeight * (1 - normalized);
      points.push((index === 0 ? "M" : "L") + px.toFixed(2) + " " + py.toFixed(2));
    });
    const thresholdY = top + plotHeight * (1 - Math.min(1, input.backgroundCm3 / result.peakCm3));
    const crossingX = result.rightCrossingNm === null ? null : left + plotWidth * result.rightCrossingNm / maxX;
    const crossingTextX = crossingX === null ? null : crossingX < left + 65 ? crossingX + 6 : crossingX - 6;
    const crossingTextAnchor = crossingX !== null && crossingX < left + 65 ? "start" : "end";
    svg.innerHTML =
      '<title>' + yLabel + '</title><desc>' + backgroundLabel + '</desc>' +
      '<line x1="' + left + '" y1="' + (top + plotHeight) + '" x2="' + (width - right) + '" y2="' + (top + plotHeight) + '" stroke="currentColor" opacity=".35"/>' +
      '<line x1="' + left + '" y1="' + top + '" x2="' + left + '" y2="' + (top + plotHeight) + '" stroke="currentColor" opacity=".35"/>' +
      '<line x1="' + left + '" y1="' + (top + plotHeight / 2) + '" x2="' + (width - right) + '" y2="' + (top + plotHeight / 2) + '" stroke="currentColor" opacity=".14"/>' +
      '<path d="' + points.join(" ") + '" fill="none" stroke="#b94f32" stroke-width="3" stroke-linecap="round"/>' +
      (result.rightCrossingNm === null ? "" :
        '<line x1="' + left + '" y1="' + thresholdY.toFixed(2) + '" x2="' + (width - right) + '" y2="' + thresholdY.toFixed(2) + '" stroke="#236c68" stroke-dasharray="6 5" stroke-width="1.5"/>' +
        '<line data-crossing-marker x1="' + crossingX.toFixed(2) + '" y1="' + top + '" x2="' + crossingX.toFixed(2) + '" y2="' + (top + plotHeight) + '" stroke="#236c68" stroke-dasharray="3 4" stroke-width="1.5"/>' +
        '<text x="' + crossingTextX.toFixed(2) + '" y="' + (top + 30) + '" text-anchor="' + crossingTextAnchor + '" fill="#236c68" font-size="13">x*</text>') +
      '<text x="' + left + '" y="' + (height - 10) + '" fill="currentColor" font-size="12">' + xLabel + ' 0</text>' +
      '<text x="' + (width - right - 62) + '" y="' + (height - 10) + '" fill="currentColor" font-size="12">' + maxX.toPrecision(3) + ' nm</text>' +
      '<text x="' + (left + 8) + '" y="' + (top + 15) + '" fill="currentColor" font-size="12">100%</text>' +
      '<text x="8" y="' + (top + 8) + '" fill="currentColor" font-size="12">' + yLabel + '</text>';
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);
  }

  function initDependencyExplorer() {
    const rootEl = document.querySelector("[data-dependency-explorer]");
    if (!rootEl) return;
    const select = rootEl.querySelector("select");
    const output = rootEl.querySelector("[data-dependency-output]");
    const nodes = Array.from(rootEl.querySelectorAll("[data-dependency-node]"));
    const relations = Array.from(rootEl.querySelectorAll("[data-relation-case]"));
    const cases = {
      gate: {
        active: ["device", "gate", "thermal", "contact"],
        text: rootEl.dataset.gateText
      },
      contact: {
        active: ["pattern", "etch", "contact", "metal"],
        text: rootEl.dataset.contactText
      },
      interconnect: {
        active: ["thermal", "gate", "metal", "reliability"],
        text: rootEl.dataset.interconnectText
      }
    };
    function update() {
      const choice = cases[select.value];
      nodes.forEach(function (node) { node.dataset.active = String(choice.active.includes(node.dataset.dependencyNode)); });
      output.textContent = choice.text;
      relations.forEach(function (list) { list.hidden = list.dataset.relationCase !== select.value; });
    }
    select.addEventListener("change", update);
    update();
  }

  function initEvidenceChallenge() {
    const rootEl = document.querySelector("[data-evidence-challenge]");
    if (!rootEl) return;
    rootEl.querySelectorAll("[data-evidence-choice]").forEach(function (button) {
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", function () {
        rootEl.querySelectorAll("[data-evidence-choice]").forEach(function (other) { other.setAttribute("aria-pressed", "false"); });
        button.setAttribute("aria-pressed", "true");
        rootEl.querySelector("[data-evidence-feedback]").textContent = button.dataset.feedback;
      });
    });
  }
})();
