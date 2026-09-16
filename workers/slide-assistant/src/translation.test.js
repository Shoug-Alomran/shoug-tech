import test from 'node:test';
import assert from 'node:assert/strict';
import { webcrypto } from 'node:crypto';
import worker from './index.js';
import { validateTexts, parseTranslation } from './translation.js';
if (!globalThis.crypto) globalThis.crypto = webcrypto;
const endpoint = 'https://worker.test/v1/breakdown-translation';
function request(body, origin = 'http://localhost:8000') {
  return new Request(endpoint, { method: 'POST', headers: { origin, 'content-type': 'application/json' }, body: JSON.stringify(body) });
}

test('validates bounded non-empty text batches', () => {
  assert.equal(validateTexts(['Information security', 'Risk assessment']), true);
  for (const texts of [[], [''], [9], ['x'.repeat(4001)], Array(51).fill('hello'), ['a'.repeat(4000), 'b'.repeat(3000)]]) assert.equal(validateTexts(texts), false);
});
test('rejects missing, untranslated, or malformed model output', () => {
  assert.deepEqual(parseTranslation('["أمن المعلومات"]', ['Information security']), ['أمن المعلومات']);
  assert.deepEqual(parseTranslation('["CIA","TCP/IP"]', ['CIA', 'TCP/IP']), ['CIA', 'TCP/IP']);
  assert.deepEqual(parseTranslation('["https://example.com","student@example.com","guide.pdf"]', ['https://example.com', 'student@example.com', 'guide.pdf']), ['https://example.com', 'student@example.com', 'guide.pdf']);
  for (const text of ['[]', '["Information security"]', '[null]', 'not json']) assert.throws(() => parseTranslation(text, ['Information security']));
});
test('translation route returns Arabic with site CORS', async () => {
  const response = await worker.fetch(request({ texts: ['Information security'] }), {
    AI: { run: async (_model, input) => {
      assert.equal(input.chat_template_kwargs.enable_thinking, false);
      return { response: '["أمن المعلومات"]' };
    } }
  });
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('access-control-allow-origin'), 'http://localhost:8000');
  assert.deepEqual(await response.json(), { translations: ['أمن المعلومات'] });
});
test('bad input, untrusted origins, rate limits and incomplete output do not succeed', async () => {
  assert.equal((await worker.fetch(request({ texts: [] }), {})).status, 400);
  assert.equal((await worker.fetch(request({ texts: ['hello'] }, 'https://untrusted.test'), {})).status, 403);
  assert.equal((await worker.fetch(request({ texts: ['hello'] }), { TRANSLATION_RATE_LIMIT: { limit: async () => ({ success: false }) } })).status, 429);
  assert.equal((await worker.fetch(request({ texts: ['hello'] }), { AI: { run: async () => ({ response: '["hello"]' }) } })).status, 502);
});

test('repairs only untranslated titles, names and mnemonics before returning a complete batch', async () => {
  let calls = 0;
  const response = await worker.fetch(request({ texts: ['Learning objectives', '4+1\n View Model', 'Kruchten, 1995', 'Lions Prefer Dark Pizza'] }), {
    AI: { run: async (_model, input) => {
      calls++;
      const texts = JSON.parse(input.messages.at(-1).content);
      if (calls === 1) {
        assert.equal(texts[1], '4+1 View Model');
        return { response: JSON.stringify(['أهداف التعلم', '4+1 View Model', 'Kruchten, 1995', 'Lions Prefer Dark Pizza']) };
      }
      assert.deepEqual(texts, ['4+1 View Model', 'Kruchten, 1995', 'Lions Prefer Dark Pizza']);
      return { response: JSON.stringify(['نموذج الرؤى 4+1', 'كروشتن، 1995', 'الأسود تفضل البيتزا الداكنة']) };
    } }
  });
  assert.equal(response.status, 200);
  assert.equal(calls, 2);
  assert.deepEqual((await response.json()).translations, ['أهداف التعلم', 'نموذج الرؤى 4+1', 'كروشتن، 1995', 'الأسود تفضل البيتزا الداكنة']);
});
