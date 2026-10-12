const { test, expect } = require("@playwright/test");

async function collectBrowserErrors(page) {
  const errors = [];
  page.on("pageerror", error => errors.push(error.message));
  page.on("console", message => {
    if (message.type() === "error") errors.push(message.text());
  });
  return errors;
}

async function expectNoOverflow(page) {
  const dimensions = await page.evaluate(() => {
    const viewport = document.documentElement.clientWidth;
    return {
      viewport,
      content: document.documentElement.scrollWidth,
      offenders: Array.from(document.querySelectorAll("body *"))
        .map(element => ({
          tag: element.tagName.toLowerCase(),
          className: typeof element.className === "string" ? element.className : "",
          right: Math.round(element.getBoundingClientRect().right),
          text: (element.textContent || "").trim().slice(0, 50)
        }))
        .filter(element => element.right > viewport + 1)
        .slice(0, 8)
    };
  });
  expect(dimensions.content, JSON.stringify(dimensions.offenders)).toBeLessThanOrEqual(dimensions.viewport + 1);
}

test("English home, searchable chapter guide, and source pages load without browser errors", async ({ page }) => {
  const errors = await collectBrowserErrors(page);
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("./");
  await expect(page.getByRole("button", { name: "Open navigation" })).toBeHidden();
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Technology is decided");
  await expect(page.locator("[data-chapter-card]")).toHaveCount(13);
  await page.getByLabel("Find a chapter").fill("thermal history");
  await expect(page.locator("[data-chapter-card]:visible")).toHaveCount(1);
  await page.getByLabel("Find a chapter").fill("no-such-topic");
  await expect(page.getByRole("status")).toContainText("No chapters match");
  await page.goto("./references.html");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("References");
  expect(errors).toEqual([]);
});

test("Korean routes provide translated navigation, chapter search, and a working language switch", async ({ page }) => {
  const errors = await collectBrowserErrors(page);
  await page.goto("./ko/");
  await expect(page.locator("html")).toHaveAttribute("lang", "ko");
  await expect(page.getByRole("navigation").getByRole("link", { name: "장 목록" })).toBeVisible();
  const firstChapterCard = page.locator("[data-chapter-card]").first();
  await expect(firstChapterCard.locator("p")).toContainText("통합 의사결정");
  await expect(firstChapterCard.locator("p")).not.toContainText("integration decision");
  await page.getByLabel("장 찾기").fill("통합 의사결정");
  await expect(page.locator("[data-chapter-card]:visible")).toHaveCount(1);
  await page.getByLabel("장 찾기").fill("변동 전파");
  await expect(page.locator("[data-chapter-card]:visible")).toHaveCount(1);
  await page.getByRole("link", { name: "English" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  expect(errors).toEqual([]);
});

test("chapter locale links preserve the selected chapter and advertise matching alternates", async ({ page }) => {
  await page.goto("./chapters/c06-junction-thermal-history.html");
  await expect(page.locator('link[hreflang="en"]')).toHaveAttribute(
    "href",
    "https://frbread7.github.io/processintegrationbook/chapters/c06-junction-thermal-history.html"
  );
  await expect(page.locator('link[hreflang="ko"]')).toHaveAttribute(
    "href",
    "https://frbread7.github.io/processintegrationbook/ko/chapters/c06-junction-thermal-history.html"
  );
  await page.getByRole("link", { name: "한국어" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "ko");
  await expect(page).toHaveURL(/\/ko\/chapters\/c06-junction-thermal-history\.html$/);
  await expect(page.getByRole("heading", { level: 1 })).toContainText("접합");
  await page.getByRole("link", { name: "English" }).click();
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await expect(page).toHaveURL(/\/chapters\/c06-junction-thermal-history\.html$/);
});

test("desktop thermal lab returns the analytical reference case and rejects invalid input", async ({ page }) => {
  const errors = await collectBrowserErrors(page);
  await page.goto("./lab.html");
  const output = page.locator("[data-thermal-output]");
  const status = page.locator("[data-thermal-status]");
  await expect(output).toContainText("24.523 nm");
  await expect(output).toContainText("163.413 nm");
  await expect(status).not.toContainText("Literature caution");
  await page.getByLabel("Initial sigma (nm)").fill("0.5");
  await page.getByLabel("Areal dose (cm⁻²)").fill("1000000000000000");
  await page.getByLabel("Temperature (°C)").fill("850");
  await page.getByLabel("Duration (s)").fill("0.1");
  await expect(status).toContainText("Fair (1975) reports concentration-dependent profiles");
  await expect(status).toContainText("neutral ambients");
  await expect(status).toContainText("does not reproduce those conditions");
  await page.getByRole("button", { name: "Add a hold" }).click();
  await expect(page.locator("[data-hold-list] .hold-row")).toHaveCount(2);
  await page.locator("[data-hold-list] [data-remove-hold]").last().click();
  await expect(page.locator("[data-hold-list] .hold-row")).toHaveCount(1);
  await page.getByLabel("Temperature (°C)").fill("849");
  await expect(page.getByRole("status")).toContainText("850");
  await page.getByRole("button", { name: "Reset reference case" }).click();
  await expect(output).toContainText("24.523 nm");
  await expect(status).not.toContainText("Literature caution");
  const addHold = page.getByRole("button", { name: "Add a hold" });
  await expect(page.locator("#hold-limit-note")).toContainText("Up to 30 holds");
  for (let index = 0; index < 29; index += 1) await addHold.click();
  await expect(page.locator("[data-hold-list] .hold-row")).toHaveCount(30);
  await expect(addHold).toBeDisabled();
  await page.locator("[data-hold-list] [data-remove-hold]").last().click();
  await expect(page.locator("[data-hold-list] .hold-row")).toHaveCount(29);
  await expect(addHold).toBeEnabled();
  expect(errors).toEqual([]);
});

test("Korean thermal lab localizes the concentration literature caution", async ({ page }) => {
  await page.goto("./ko/lab.html");
  const status = page.locator("[data-thermal-status]");
  await expect(status).not.toContainText("문헌상 주의");
  await page.getByLabel("초기 시그마 (nm)").fill("0.5");
  await page.getByLabel("면적 선량 (cm⁻²)").fill("1000000000000000");
  await page.getByLabel("온도 (°C)").fill("850");
  await page.getByLabel("시간 (s)").fill("0.1");
  await expect(status).toContainText("중성 분위기의 고농도 보론 확산");
  await expect(status).toContainText("해당 조건을 재현하지 않으며");
  await page.getByLabel("온도 (°C)").fill("849");
  await expect(status).toContainText("결과가 없습니다");
  await expect(status).not.toContainText("Temperature");
  await expect(page.locator("[data-thermal-output]")).toContainText("결과가 없습니다");
});

test("qualitative integration activities respond with explicit reasoning limits", async ({ page }) => {
  const errors = await collectBrowserErrors(page);
  await page.goto("./lab.html");
  await page.getByLabel("Review focus").selectOption("interconnect");
  await expect(page.locator('[data-dependency-node="gate"]')).toHaveAttribute("data-active", "true");
  await expect(page.locator('[data-dependency-node="reliability"]')).toHaveAttribute("data-active", "true");
  await page.getByLabel("Review focus").selectOption("contact");
  await expect(page.locator("[data-dependency-output]")).toContainText("pattern definition");
  await page.locator('[data-evidence-choice="c"]').click();
  await expect(page.locator("[data-evidence-feedback]")).toContainText("competing hypotheses");
  expect(errors).toEqual([]);
});

test("tablet chapter layout and knowledge check stay usable", async ({ page }) => {
  const errors = await collectBrowserErrors(page);
  await page.setViewportSize({ width: 768, height: 1024 });
  await page.goto("./chapters/c06-junction-thermal-history.html");
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/junction evolution/i);
  await page.locator('[data-quiz] button[data-correct="true"]').click();
  await expect(page.locator(".quiz-feedback")).toContainText("Correct");
  await expectNoOverflow(page);
  expect(errors).toEqual([]);
});

test("mobile navigation, theme toggle, and lab content fit a phone viewport", async ({ page }) => {
  const errors = await collectBrowserErrors(page);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("./");
  await expectNoOverflow(page);
  await page.getByRole("button", { name: "Open navigation" }).click();
  await page.getByRole("navigation").getByRole("link", { name: "Lab" }).click();
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Integration laboratory");
  await page.waitForLoadState("load");
  await page.getByRole("button", { name: "Theme" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expectNoOverflow(page);
  expect(errors).toEqual([]);
});
