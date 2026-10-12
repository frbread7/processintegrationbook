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
  await expect(output).toContainText("24.523 nm");
  await expect(output).toContainText("163.413 nm");
  await page.getByRole("button", { name: "Add a hold" }).click();
  await expect(page.locator("[data-hold-list] .hold-row")).toHaveCount(2);
  await page.locator("[data-hold-list] [data-remove-hold]").last().click();
  await expect(page.locator("[data-hold-list] .hold-row")).toHaveCount(1);
  await page.getByLabel("Temperature (°C)").fill("849");
  await expect(page.getByRole("status")).toContainText("850");
  await page.getByRole("button", { name: "Reset reference case" }).click();
  await expect(output).toContainText("24.523 nm");
  expect(errors).toEqual([]);
});

test("qualitative integration activities respond with explicit reasoning limits", async ({ page }) => {
  const errors = await collectBrowserErrors(page);
  await page.goto("./lab.html");
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
  await page.getByRole("button", { name: "Theme" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expectNoOverflow(page);
  expect(errors).toEqual([]);
});
