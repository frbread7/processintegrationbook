const { defineConfig } = require("@playwright/test");

const externalBaseURL = process.env.BASE_URL;

module.exports = defineConfig({
  testDir: "./tests/browser",
  fullyParallel: true,
  reporter: "list",
  retries: process.env.CI ? 1 : 0,
  use: {
    baseURL: externalBaseURL || "http://127.0.0.1:8173/",
    browserName: "chromium",
    trace: "retain-on-failure",
    screenshot: "only-on-failure"
  },
  webServer: externalBaseURL ? undefined : {
    command: "python3 -m http.server 8173 --directory site",
    url: "http://127.0.0.1:8173/",
    reuseExistingServer: !process.env.CI,
    timeout: 30000
  }
});
