import test from "node:test";
import assert from "node:assert/strict";
import { verifyIdToken } from "./firebase-token.js";

const b64 = (data) =>
  Buffer.from(typeof data === "string" ? data : new Uint8Array(data))
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");

const pair = await crypto.subtle.generateKey(
  { name: "RSASSA-PKCS1-v1_5", modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" },
  true,
  ["sign", "verify"],
);
const jwk = { ...(await crypto.subtle.exportKey("jwk", pair.publicKey)), kid: "k1" };
const now = 1_800_000_000;

async function sign(claims, kid = "k1") {
  const head = b64(JSON.stringify({ alg: "RS256", kid, typ: "JWT" }));
  const body = b64(JSON.stringify(claims));
  const sig = await crypto.subtle.sign("RSASSA-PKCS1-v1_5", pair.privateKey, new TextEncoder().encode(`${head}.${body}`));
  return `${head}.${body}.${b64(sig)}`;
}
const good = {
  iss: "https://securetoken.google.com/shoug-tech",
  aud: "shoug-tech",
  sub: "user-1",
  email: "s@example.com",
  iat: now - 60,
  auth_time: now - 600,
  exp: now + 3000,
};
const opts = { keys: [jwk], now };

test("a correctly signed Firebase token is accepted", async () => {
  assert.deepEqual(await verifyIdToken(await sign(good), opts), { uid: "user-1", email: "s@example.com" });
});

test("tampered, foreign, expired or unknown-key tokens are rejected", async () => {
  const token = await sign(good);
  const [h, , s] = token.split(".");
  const forged = `${h}.${b64(JSON.stringify({ ...good, sub: "someone-else" }))}.${s}`;
  assert.equal(await verifyIdToken(forged, opts), null);
  assert.equal(await verifyIdToken(await sign({ ...good, aud: "other-project" }), opts), null);
  assert.equal(await verifyIdToken(await sign({ ...good, iss: "https://evil.example" }), opts), null);
  assert.equal(await verifyIdToken(await sign({ ...good, exp: now - 1 }), opts), null);
  assert.equal(await verifyIdToken(await sign(good, "unknown"), opts), null);
  assert.equal(await verifyIdToken("not-a-token", opts), null);
});
