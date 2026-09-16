/* Opt-in end-to-end test against a PUBLIC lesson and the real translation API.
 * Uses a fresh, signed-out browser. No local course files are uploaded.
 * node scripts/test_breakdown_translation_live.cjs https://shoug-tech.com/.../lesson.html
 */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const url = new URL(process.argv[2]);
assert.equal(url.origin, 'https://shoug-tech.com');
assert.ok(url.pathname.includes('/slide-breakdowns/') && url.pathname.endsWith('.html'));
async function main() {
  const browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE } : {}) });
  try {
    const page = await browser.newPage();
    // Preview only the pending controller/style over the already-public lesson.
    // Lesson text still comes exclusively from the public URL above.
    if (process.env.BREAKDOWN_TEST_LOCAL_ASSETS === '1') {
      const path = require('node:path');
      for (const [asset, contentType] of [['javascripts/breakdown-language.js', 'text/javascript'], ['styles/breakdown-language.css', 'text/css']]) {
        await page.route('**/' + asset + '*', route => route.fulfill({
          path: path.join(__dirname, '../docs', asset), contentType
        }));
      }
    }
    const failures = [], responses = [];
    page.on('response', response => {
      if (!response.url().includes('/v1/breakdown-translation')) return;
      responses.push(response.status());
      if (!response.ok()) {
        failures.push(response.status());
        if (process.env.BREAKDOWN_FAILURE_PATH) require('node:fs').writeFileSync(process.env.BREAKDOWN_FAILURE_PATH, response.request().postData());
      }
      console.log('Translation response:', response.status());
    });
    page.on('requestfailed', request => {
      if (request.url().includes('/v1/breakdown-translation')) failures.push(request.failure().errorText);
    });
    const result = await page.goto(url.href, { waitUntil: 'domcontentloaded' });
    assert.equal(result.status(), 200);
    const originalHeading = await page.locator('h1').first().textContent();
    const started = Date.now();
    await page.locator('[data-bd-lang=ar]').click();
    await page.waitForFunction(() => document.querySelector('.bd-language').getAttribute('aria-busy') === 'false', {}, { timeout: 300000 });
    const status = await page.locator('.bd-language-status').textContent();
    assert.equal(await page.locator('html').getAttribute('lang'), 'ar', status);
    const arabicHeading = await page.locator('h1').first().textContent();
    assert.match(arabicHeading, /[\u0600-\u06ff]/);
    if (originalHeading.includes('4+1')) assert.ok(arabicHeading.includes('4+1'), 'The title must keep the 4+1 model identity');
    const counts = await page.locator('body').evaluate(body => {
      const text = body.innerText;
      return { arabic: (text.match(/[\u0600-\u06ff]/g) || []).length, latin: (text.match(/[A-Za-z]/g) || []).length };
    });
    assert.ok(counts.arabic > counts.latin, 'Lesson prose must actually become Arabic');
    assert.deepEqual(failures, []);
    if (process.env.BREAKDOWN_SCREENSHOT) await page.screenshot({ path: process.env.BREAKDOWN_SCREENSHOT });
    await page.locator('[data-bd-lang=en]').click();
    assert.equal(await page.locator('h1').first().textContent(), originalHeading);
    console.log(JSON.stringify({ result: 'PASS', url: url.href, arabicHeading, localAssets: process.env.BREAKDOWN_TEST_LOCAL_ASSETS === '1', batches: responses.length, seconds: (Date.now() - started) / 1000, ...counts }));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
