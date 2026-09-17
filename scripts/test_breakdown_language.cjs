/* Run against a local docs server. Set NODE_PATH to a Playwright installation. */
const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const base = process.env.BREAKDOWN_TEST_URL || "http://127.0.0.1:8765";
async function main() {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
      ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE }
      : {}),
  });
  try {
    const context = await browser.newContext();
    let fail = false,
      delay = 0,
      calls = 0;
    await context.route("**/*", async (route) => {
      if (route.request().url().includes("/v1/breakdown-translation")) {
        calls++;
        assert.ok(!route.request().frame().url().endsWith("/index.html"));
        if (delay) await new Promise((resolve) => setTimeout(resolve, delay));
        const { texts } = route.request().postDataJSON();
        assert.ok(!texts.some((text) => text.includes("PRIVATE_TEST_TEXT")));
        return route.fulfill({
          status: fail ? 503 : 200,
          contentType: "application/json",
          body: JSON.stringify({
            translations: texts.map((_, i) => "نص عربي للاختبار " + i),
          }),
        });
      }
      if (!route.request().url().startsWith(base)) return route.abort();
      return route.continue();
    });
    const page = await context.newPage();
    // The site shell owns no lesson controls or translation requests.
    for (const shell of [
      "/academics/cybersecurity/cys403/slide-breakdowns/01-chapter-1-security-risk-management-governance-and-control/index.html",
      "/academics/software-engineering/se322/slide-breakdowns/04-chapter-2-software-architecture-lecture-3-extra/index.html",
    ]) {
      await page.goto(base + shell);
      const heading = await page.locator("h1").first().textContent();
      const shellLang = await page.locator("html").getAttribute("lang");
      let globalPreference = await page.evaluate(() =>
        localStorage.getItem("shoug-lang"),
      );
      assert.equal(await page.locator(".bd-language").count(), 0);
      await page.locator("[data-lang-toggle]:visible").first().waitFor();
      assert.equal(await page.locator("[data-lang-toggle]:visible").count(), 1);
      // The original site control still changes the shell language.
      const globalToggle = page.locator("[data-lang-toggle]:visible").first();
      await globalToggle.click();
      await page.waitForFunction(() =>
        document.documentElement.lang.startsWith("ar"),
      );
      await globalToggle.click();
      await page.waitForFunction(
        () => !document.documentElement.lang.startsWith("ar"),
      );
      globalPreference = await page.evaluate(() =>
        localStorage.getItem("shoug-lang"),
      );
      const embedded = page.locator("iframe").first();
      await embedded.scrollIntoViewIfNeeded();
      const lesson = await (await embedded.elementHandle()).contentFrame();
      await lesson.locator("[data-bd-lang=ar]").click();
      await lesson.waitForFunction(
        () => document.documentElement.lang === "ar",
      );
      assert.equal(await page.locator(".bd-language").count(), 0);
      assert.equal(await page.locator("h1").first().textContent(), heading);
      assert.equal(await page.locator("html").getAttribute("lang"), shellLang);
      assert.equal(
        await page.evaluate(() => localStorage.getItem("shoug-lang")),
        globalPreference,
      );
      await lesson.locator("[data-bd-lang=en]").click();
      console.log(
        "PASS controls and translation stay inside the lesson:",
        shell,
      );
    }
    await page.goto(
      base +
        "/academics/software-engineering/se322/slide-breakdowns/index.html",
    );
    assert.equal(await page.locator(".bd-language").count(), 0);
    const samplePaths = [
      "docs/academics/cybersecurity/cys403/slide-breakdowns/01-chapter-1-security-risk-management-governance-and-control/chapter-1-security-risk-management-governance-and-control.html",
      "docs/academics/cybersecurity/cys401/slide-breakdowns/01-chapter-1-introduction-to-cybersecurity/chapter-1.html",
      "docs/academics/software-engineering/se311/slide-breakdowns/01-chapter-1-basics-of-requirements-engineering/chapter-1/chapter-1.html",
    ];
    for (const file of samplePaths) {
      await page.goto(base + "/" + file.slice(5) + "?lang=en");
      await page.locator(".bd-language").waitFor();
      assert.notEqual(
        await page
          .locator(".bd-language")
          .evaluate((el) => getComputedStyle(el).position),
        "fixed",
      );
      if (await page.locator(".bdx-bar-inner").count()) {
        assert.equal(
          await page.locator(".bdx-bar-inner > .bd-language").count(),
          1,
        );
        for (const width of [1440, 375]) {
          await page.setViewportSize({ width, height: 900 });
          const control = await page.locator(".bd-language").boundingBox();
          const header = await page.locator(".bdx-bar").boundingBox();
          assert.ok(control.x >= 0 && control.x + control.width <= width);
          assert.ok(
            control.y >= header.y &&
              control.y + control.height <= header.y + header.height,
          );
        }
        await page.screenshot({
          path: "/private/tmp/breakdown-toolbar-mobile.png",
        });
        await page.setViewportSize({ width: 1440, height: 900 });
        await page.screenshot({
          path: "/private/tmp/breakdown-toolbar-desktop.png",
        });
      }
      const original = await page.locator("h1").first().textContent();
      await page.locator("[data-bd-lang=ar]").click();
      await page.waitForFunction(
        () =>
          document.documentElement.lang === "ar" &&
          document.querySelector(".bd-language").getAttribute("aria-busy") ===
            "false",
      );
      assert.equal(await page.locator("html").getAttribute("dir"), "rtl");
      assert.match(await page.locator("h1").first().textContent(), /نص عربي/);
      // Wrapper language changes reach its standalone iframe.
      const frame = page
        .frames()
        .find(
          (frame) =>
            frame !== page.mainFrame() &&
            frame.url().includes("slide-breakdowns"),
        );
      if (frame)
        await frame.waitForFunction(
          () => document.documentElement.lang === "ar",
        );
      await page.locator("[data-bd-lang=en]").click();
      assert.equal(await page.locator("h1").first().textContent(), original);
      assert.equal(await page.locator("html").getAttribute("dir"), "ltr");
      if (frame)
        await frame.waitForFunction(
          () => document.documentElement.lang === "en",
        );
      console.log("PASS English/Arabic/English:", file);
    }
    await page.evaluate(() => {
      sessionStorage.clear();
      Object.keys(localStorage)
        .filter((k) => k.startsWith("bd-ar-"))
        .forEach((k) => localStorage.removeItem(k));
    });
    await page.reload();
    fail = true;
    await page.locator("[data-bd-lang=ar]").click();
    await page.waitForFunction(() =>
      document
        .querySelector(".bd-language-status")
        .textContent.includes("Translation failed"),
    );
    assert.equal(await page.locator("html").getAttribute("lang"), "en");
    assert.ok((await page.locator(".bd-language").boundingBox()).height < 60);
    fail = false;
    await page.locator("[data-bd-lang=ar]").click();
    await page.waitForFunction(() => document.documentElement.lang === "ar");
    await page.reload();
    await page.waitForFunction(() => document.documentElement.lang === "ar");
    await page.evaluate(() => {
      const p = document.createElement("p");
      p.id = "dynamic-test";
      p.textContent = "A newly revealed explanation";
      document.body.append(p);
      const privateNotes = document.createElement("div");
      privateNotes.id = "shoug-notes-panel";
      privateNotes.textContent = "PRIVATE_TEST_TEXT";
      document.body.append(privateNotes);
      const input = document.createElement("input");
      input.id = "placeholder-test";
      input.placeholder = "Search this lesson";
      document.body.append(input);
    });
    await page.waitForFunction(() =>
      document.getElementById("dynamic-test").textContent.includes("نص عربي"),
    );
    await page.waitForFunction(() =>
      document
        .getElementById("placeholder-test")
        .placeholder.includes("نص عربي"),
    );
    await page.locator("[data-bd-lang=en]").click();
    assert.equal(
      await page.locator("#placeholder-test").getAttribute("placeholder"),
      "Search this lesson",
    );
    assert.equal(
      await page.locator("#dynamic-test").textContent(),
      "A newly revealed explanation",
    );
    await page.evaluate(() => {
      sessionStorage.clear();
      Object.keys(localStorage)
        .filter((k) => k.startsWith("bd-ar-"))
        .forEach((k) => localStorage.removeItem(k));
    });
    await page.reload();
    delay = 500;
    await page.locator("[data-bd-lang=ar]").click();
    await page.locator("[data-bd-lang=en]").click();
    await page.waitForTimeout(700);
    assert.equal(await page.locator("html").getAttribute("lang"), "en");
    delay = 0;
    await page.setViewportSize({ width: 375, height: 812 });
    const box = await page.locator(".bd-language").boundingBox();
    assert.ok(box.x >= 0 && box.x + box.width <= 375);
    console.log(
      "PASS errors, retry, dynamic content, request cancellation, mobile controls; requests:",
      calls,
    );
  } finally {
    await browser.close();
  }
}
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
