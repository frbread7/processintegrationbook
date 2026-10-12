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

    function makeHold(hold) {
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
        if (holdList.children.length > 1) row.remove();
        calculate();
      });
      holdList.appendChild(row);
    }

    function currentInput() {
      const fields = {};
      rootEl.querySelectorAll("[data-profile-input]").forEach(function (field) {
        fields[field.dataset.profileInput] = Number(field.value);
      });
      fields.holds = Array.from(holdList.querySelectorAll(".hold-row")).map(function (row) {
        return {
          tempC: Number(row.querySelector("[data-hold-temp]").value),
          timeS: Number(row.querySelector("[data-hold-time]").value)
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
        status.textContent = result.surfaceTruncationLikely ? rootEl.dataset.surfaceWarning : rootEl.dataset.modelStatus;
        drawChart(chart, input, result, model, rootEl.dataset.chartXLabel, rootEl.dataset.chartYLabel, rootEl.dataset.backgroundLabel);
      } catch (error) {
        output.textContent = rootEl.dataset.invalidResult;
        status.textContent = error.message;
        chart.replaceChildren();
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
    addButton.addEventListener("click", function () { makeHold({ tempC: 950, timeS: 10 }); calculate(); });
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
    const maxX = Math.max(220, input.projectedRangeNm + 4.5 * sigma);
    const maxXBounded = Math.min(maxX, 1000);
    const points = [];
    for (let i = 0; i <= 120; i += 1) {
      const x = maxXBounded * i / 120;
      const c = model.concentrationAtNm(x, input, result);
      const normalized = Math.min(1, c / result.peakCm3);
      const px = left + plotWidth * x / maxXBounded;
      const py = top + plotHeight * (1 - normalized);
      points.push((i === 0 ? "M" : "L") + px.toFixed(2) + " " + py.toFixed(2));
    }
    const thresholdY = top + plotHeight * (1 - Math.min(1, input.backgroundCm3 / result.peakCm3));
    svg.innerHTML =
      '<title>' + yLabel + '</title><desc>' + backgroundLabel + '</desc>' +
      '<line x1="' + left + '" y1="' + (top + plotHeight) + '" x2="' + (width - right) + '" y2="' + (top + plotHeight) + '" stroke="currentColor" opacity=".35"/>' +
      '<line x1="' + left + '" y1="' + top + '" x2="' + left + '" y2="' + (top + plotHeight) + '" stroke="currentColor" opacity=".35"/>' +
      '<line x1="' + left + '" y1="' + (top + plotHeight / 2) + '" x2="' + (width - right) + '" y2="' + (top + plotHeight / 2) + '" stroke="currentColor" opacity=".14"/>' +
      '<path d="' + points.join(" ") + '" fill="none" stroke="#b94f32" stroke-width="3" stroke-linecap="round"/>' +
      (result.rightCrossingNm === null ? "" :
        '<line x1="' + left + '" y1="' + thresholdY.toFixed(2) + '" x2="' + (width - right) + '" y2="' + thresholdY.toFixed(2) + '" stroke="#236c68" stroke-dasharray="6 5" stroke-width="1.5"/>') +
      '<text x="' + left + '" y="' + (height - 10) + '" fill="currentColor" font-size="12">' + xLabel + ' 0</text>' +
      '<text x="' + (width - right - 62) + '" y="' + (height - 10) + '" fill="currentColor" font-size="12">' + maxXBounded.toFixed(0) + ' nm</text>' +
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
        active: ["thermal", "material", "metal", "reliability"],
        text: rootEl.dataset.interconnectText
      }
    };
    function update() {
      const choice = cases[select.value];
      nodes.forEach(function (node) { node.dataset.active = String(choice.active.includes(node.dataset.dependencyNode)); });
      output.textContent = choice.text;
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
