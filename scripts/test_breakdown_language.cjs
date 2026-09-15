/* Run against a local docs server. Set NODE_PATH to a Playwright installation. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BREAKDOWN_TEST_URL || 'http://127.0.0.1:8765';
async function main() {
  const browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE } : {}) });
  try {
    const context = await browser.newContext();
    let fail = false, delay = 0, calls = 0;
    await context.route('**/*', async route => {
      if (route.request().url().includes('/v1/breakdown-translation')) {
        calls++;
        if (delay) await new Promise(resolve => setTimeout(resolve, delay));
        const { texts } = route.request().postDataJSON();
        assert.ok(!texts.some(text => text.includes('PRIVATE_TEST_TEXT')));
        return route.fulfill({ status: fail ? 503 : 200, contentType: 'application/json', body: JSON.stringify({ translations: texts.map((_, i) => 'نص عربي للاختبار ' + i) }) });
      }
      if (!route.request().url().startsWith(base)) return route.abort();
      return route.continue();
    });
    const page = await context.newPage();
    const samplePaths = [
      'docs/academics/cybersecurity/cys403/slide-breakdowns/01-chapter-1-security-risk-management-governance-and-control/index.html',
      'docs/academics/cybersecurity/cys401/slide-breakdowns/01-chapter-1-introduction-to-cybersecurity/chapter-1.html',
      'docs/academics/software-engineering/se311/slide-breakdowns/01-chapter-1-basics-of-requirements-engineering/chapter-1/chapter-1.html'
    ];
    for (const file of samplePaths) {
      await page.goto(base + '/' + file.slice(5) + '?lang=en');
      await page.locator('.bd-language').waitFor();
      const original = await page.locator('h1').first().textContent();
      await page.locator('[data-bd-lang=ar]').click();
      await page.waitForFunction(() => document.documentElement.lang === 'ar' && document.querySelector('.bd-language').getAttribute('aria-busy') === 'false');
      assert.equal(await page.locator('html').getAttribute('dir'), 'rtl');
      assert.match(await page.locator('h1').first().textContent(), /نص عربي/);
      // Wrapper language changes reach its standalone iframe.
      const frame = page.frames().find(frame => frame !== page.mainFrame() && frame.url().includes('slide-breakdowns'));
      if (frame) await frame.waitForFunction(() => document.documentElement.lang === 'ar');
      await page.locator('[data-bd-lang=en]').click();
      assert.equal(await page.locator('h1').first().textContent(), original);
      assert.equal(await page.locator('html').getAttribute('dir'), 'ltr');
      if (frame) await frame.waitForFunction(() => document.documentElement.lang === 'en');
      console.log('PASS English/Arabic/English:', file);
    }
    await page.evaluate(() => sessionStorage.clear());
    await page.reload();
    fail = true;
    await page.locator('[data-bd-lang=ar]').click();
    await page.waitForFunction(() => document.querySelector('.bd-language-status').textContent.includes('Translation failed'));
    assert.equal(await page.locator('html').getAttribute('lang'), 'en');
    fail = false;
    await page.locator('[data-bd-lang=ar]').click();
    await page.waitForFunction(() => document.documentElement.lang === 'ar');
    await page.reload();
    await page.waitForFunction(() => document.documentElement.lang === 'ar');
    await page.evaluate(() => {
      const p = document.createElement('p'); p.id = 'dynamic-test'; p.textContent = 'A newly revealed explanation'; document.body.append(p);
      const privateNotes = document.createElement('div'); privateNotes.id = 'shoug-notes-panel'; privateNotes.textContent = 'PRIVATE_TEST_TEXT'; document.body.append(privateNotes);
      const input = document.createElement('input'); input.id = 'placeholder-test'; input.placeholder = 'Search this lesson'; document.body.append(input);
    });
    await page.waitForFunction(() => document.getElementById('dynamic-test').textContent.includes('نص عربي'));
    await page.waitForFunction(() => document.getElementById('placeholder-test').placeholder.includes('نص عربي'));
    await page.locator('[data-bd-lang=en]').click();
    assert.equal(await page.locator('#placeholder-test').getAttribute('placeholder'), 'Search this lesson');
    assert.equal(await page.locator('#dynamic-test').textContent(), 'A newly revealed explanation');
    await page.evaluate(() => sessionStorage.clear());
    await page.reload();
    delay = 500;
    await page.locator('[data-bd-lang=ar]').click();
    await page.locator('[data-bd-lang=en]').click();
    await page.waitForTimeout(700);
    assert.equal(await page.locator('html').getAttribute('lang'), 'en');
    delay = 0;
    await page.setViewportSize({ width: 375, height: 812 });
    const box = await page.locator('.bd-language').boundingBox();
    assert.ok(box.x >= 0 && box.x + box.width <= 375);
    console.log('PASS errors, retry, dynamic content, request cancellation, mobile controls; requests:', calls);
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
