const { test, expect } = require("@playwright/test");

const chapters = [
  "c01-integration-as-decision",
  "c02-requirements-to-architecture",
  "c03-sequence-interface-contracts",
  "c04-isolation-substrate-choices",
  "c05-gate-stack-architecture",
  "c06-junction-thermal-history",
  "c07-pattern-transfer-chain",
  "c08-contact-mol-interface",
  "c09-beol-compatibility",
  "c10-variation-propagation",
  "c11-design-technology-cooptimization",
  "c12-integration-learning-qualification",
  "c13-public-platform-case"
];

const chapterRoutes = chapters.flatMap((chapter) => [
  `./chapters/${chapter}.html`,
  `./ko/chapters/${chapter}.html`
]);

test("all reconstructed chapter routes render with valid landmarks, language links, and no browser errors", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });

  for (const route of chapterRoutes) {
    await page.goto(route);
    await expect(page.locator("main#main")).toBeVisible();
    await expect(page.locator("article h1")).toBeVisible();
    const expectedLanguage = route.startsWith("./ko/") ? "ko" : "en";
    await expect(page.locator("html")).toHaveAttribute("lang", expectedLanguage);
    await expect(page.locator('link[hreflang="en"]')).toHaveAttribute("href", new RegExp(`${chapters.find((slug) => route.includes(slug))}\\.html$`));
    await expect(page.locator('link[hreflang="ko"]')).toHaveAttribute("href", new RegExp(`${chapters.find((slug) => route.includes(slug))}\\.html$`));
  }

  expect(errors).toEqual([]);
});

test("every chapter internal fragment link resolves to a rendered target", async ({ page }) => {
  const brokenLinks = [];
  for (const route of chapterRoutes) {
    await page.goto(route);
    const missing = await page.locator('a[href*="#"]').evaluateAll((links) => links.flatMap((link) => {
      const url = new URL(link.href);
      if (!url.hash || url.origin !== window.location.origin || url.pathname !== window.location.pathname) return [];
      const id = decodeURIComponent(url.hash.slice(1));
      return document.getElementById(id) ? [] : [`${link.getAttribute("href")} (missing #${id})`];
    }));
    brokenLinks.push(...missing.map((link) => `${route}: ${link}`));
  }
  expect(brokenLinks).toEqual([]);
});

test("no-crossing chart descriptions match the visible marks in both languages", async ({ page }) => {
  for (const [route, label] of [["./lab.html", "Initial Gaussian-component σ (nm)"], ["./ko/lab.html", "초기 가우시안 성분 σ (nm)"]]) {
    await page.goto(route);
    await page.getByLabel(label).fill("100");
    await page.locator('[data-profile-input="projectedRangeNm"]').fill("0");
    await page.locator('[data-profile-input="doseCm2"]').fill("100000000000");
    await page.locator('[data-profile-input="backgroundCm3"]').fill("10000000000000000000");
    await expect(page.locator("[data-profile-chart] [data-crossing-marker]")).toHaveCount(0);
    await expect(page.locator("[data-profile-chart] line[stroke-dasharray='6 5']")).toHaveCount(0);
    const description = await page.locator("[data-profile-chart] desc").textContent();
    const caption = await page.locator(".chart-wrap figcaption").textContent();
    expect(description).toBe(caption);
    expect(caption).toContain(route.includes("/ko/") ? "표시하지" : "no threshold line");
    await page.locator('[data-profile-input="doseCm2"]').fill("");
    await expect(page.locator("[data-profile-chart]")).toBeEmpty();
    await expect(page.locator(".chart-wrap figcaption")).toContainText(route.includes("/ko/") ? "결과가 없습니다" : "No result");
  }
});

test("wide technical figures and tables remain readable and keyboard scrollable on a phone", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const chapter of [
    "c03-sequence-interface-contracts", "c04-isolation-substrate-choices", "c05-gate-stack-architecture",
    "c07-pattern-transfer-chain", "c08-contact-mol-interface", "c09-beol-compatibility",
    "c10-variation-propagation", "c11-design-technology-cooptimization", "c12-integration-learning-qualification"
  ]) {
    for (const prefix of ["./chapters/", "./ko/chapters/"]) {
      await page.goto(prefix + chapter + ".html");
      const figure = page.locator("figure.technical-figure");
      const metrics = await figure.evaluate((element) => ({
        pageWidth: document.documentElement.scrollWidth,
        viewportWidth: document.documentElement.clientWidth,
        figureWidth: element.clientWidth,
        scrollWidth: element.scrollWidth,
        smallestLabelHeight: Math.min(...[...element.querySelectorAll("svg text")].map((label) => label.getBoundingClientRect().height))
      }));
      expect(metrics.pageWidth).toBe(metrics.viewportWidth);
      expect(metrics.scrollWidth).toBeGreaterThan(metrics.figureWidth);
      expect(metrics.smallestLabelHeight).toBeGreaterThanOrEqual(11);
      await figure.focus();
      await page.keyboard.press("ArrowRight");
      await expect.poll(() => figure.evaluate((element) => element.scrollLeft)).toBeGreaterThan(0);
      if (["c03-sequence-interface-contracts", "c05-gate-stack-architecture"].includes(chapter)) {
        const table = page.locator(".table-scroll");
        await expect(table).toHaveCount(1);
        const tableMetrics = await table.evaluate((element) => ({ visible: element.clientWidth, content: element.scrollWidth }));
        if (tableMetrics.content > tableMetrics.visible) {
          await table.focus();
          await page.keyboard.press("ArrowRight");
          await expect.poll(() => table.evaluate((element) => element.scrollLeft)).toBeGreaterThan(0);
        }
      }
    }
  }
});

test("the architecture allocation worksheet is contained and keyboard scrollable on a phone", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const prefix of ["./chapters/", "./ko/chapters/"]) {
    await page.goto(prefix + "c02-requirements-to-architecture.html");
    const table = page.locator(".table-scroll");
    await expect(table).toHaveCount(1);
    const metrics = await table.evaluate((element) => ({
      pageWidth: document.documentElement.scrollWidth,
      viewportWidth: document.documentElement.clientWidth,
      visible: element.clientWidth,
      content: element.scrollWidth
    }));
    expect(metrics.pageWidth).toBe(metrics.viewportWidth);
    expect(metrics.content).toBeGreaterThan(metrics.visible);
    await table.focus();
    await page.keyboard.press("ArrowRight");
    await expect.poll(() => table.evaluate((element) => element.scrollLeft)).toBeGreaterThan(0);
  }
});

test("chapter figures expose a title and description and their containers fit desktop, tablet, and phone viewports", async ({ page }) => {
  const figureRoutes = [
    "c01-integration-as-decision", "c03-sequence-interface-contracts", "c04-isolation-substrate-choices",
    "c05-gate-stack-architecture", "c07-pattern-transfer-chain", "c08-contact-mol-interface",
    "c09-beol-compatibility", "c10-variation-propagation", "c11-design-technology-cooptimization",
    "c12-integration-learning-qualification", "c13-public-platform-case"
  ].flatMap((chapter) => [`./chapters/${chapter}.html`, `./ko/chapters/${chapter}.html`]);
  const viewports = [
    { width: 1440, height: 1000 },
    { width: 768, height: 1024 },
    { width: 390, height: 844 }
  ];

  for (const route of figureRoutes) {
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.goto(route);
      const figures = page.locator("article figure");
      await expect(figures).toHaveCount(1);
      const svg = figures.locator("svg[role='img']");
      await expect(svg).toBeVisible();
      const accessibleText = await svg.evaluate((element) => {
        const ids = (element.getAttribute("aria-labelledby") || "").split(/\s+/).filter(Boolean);
        return ids.map((id) => document.getElementById(id)?.textContent.trim() || "");
      });
      expect(accessibleText.length).toBeGreaterThanOrEqual(2);
      expect(accessibleText.every(Boolean)).toBe(true);

      const bounds = await figures.evaluate((element) => {
        const rect = element.getBoundingClientRect();
        return { left: rect.left, right: rect.right, width: rect.width, viewport: document.documentElement.clientWidth };
      });
      expect(bounds.width).toBeGreaterThan(0);
      expect(bounds.left).toBeGreaterThanOrEqual(-1);
      expect(bounds.right).toBeLessThanOrEqual(bounds.viewport + 1);
    }
  }
});

test("the source-bounded process sequence stays legible and keyboard scrollable on a phone", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("./chapters/c13-public-platform-case.html");
  const figure = page.locator("figure.process-sequence-figure");
  await expect(figure).toBeVisible();
  const metrics = await figure.evaluate((element) => {
    const label = [...element.querySelectorAll("tspan")].find((node) => node.textContent.includes("PMOS metal"));
    return {
      viewportWidth: element.clientWidth,
      diagramWidth: element.querySelector("svg").getBoundingClientRect().width,
      scrollWidth: element.scrollWidth,
      labelHeight: label.getBoundingClientRect().height
    };
  });
  expect(metrics.diagramWidth).toBeGreaterThanOrEqual(899);
  expect(metrics.scrollWidth).toBeGreaterThan(metrics.viewportWidth);
  expect(metrics.labelHeight).toBeGreaterThanOrEqual(11);
  await figure.focus();
  await page.keyboard.press("ArrowRight");
  await expect.poll(() => figure.evaluate((element) => element.scrollLeft)).toBeGreaterThan(0);
});

test("chapter knowledge checks can be reached and answered from the keyboard", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("./chapters/c06-junction-thermal-history.html");
  await page.keyboard.press("Tab");
  await expect(page.locator(":focus")).toHaveAttribute("class", "skip-link");
  const correctAnswer = page.locator('[data-quiz] button[data-correct="true"]');
  await correctAnswer.focus();
  await page.keyboard.press("Shift+Tab");
  await page.keyboard.press("Tab");
  await expect(correctAnswer).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.locator(".quiz-feedback")).toContainText("Correct");
  await expect(page.locator(".quiz-explanation")).toBeVisible();
});
