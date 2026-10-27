// Verifies Firebase sign-in (ID) tokens in the Worker itself, the way the
// Firebase Admin SDK does: an RS256 signature checked against Google's
// published public keys, plus the issuer, audience and time claims.
//
// The earlier check sent the token to identitytoolkit with the site's web API
// key, but that key only accepts requests from the site's own pages, so every
// call from the Worker came back API_KEY_HTTP_REFERRER_BLOCKED.

export const PROJECT_ID = "shoug-tech";
const JWKS_URL =
  "https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com";
// Allowed clock difference between Google and this Worker, in seconds.
const SKEW = 300;

let cached = { keys: null, expires: 0 };

async function googleKeys() {
  if (cached.keys && Date.now() < cached.expires) return cached.keys;
  const response = await fetch(JWKS_URL);
  if (!response.ok) throw new Error(`Google keys ${response.status}`);
  const maxAge = /max-age=(\d+)/.exec(
    response.headers.get("cache-control") || "",
  );
  const { keys } = await response.json();
  cached = {
    keys,
    expires: Date.now() + (maxAge ? Number(maxAge[1]) : 3600) * 1000,
  };
  return keys;
}

function bytes(part) {
  const base64 = part.replace(/-/g, "+").replace(/_/g, "/");
  const binary = atob(base64 + "=".repeat((4 - (base64.length % 4)) % 4));
  return Uint8Array.from(binary, (c) => c.charCodeAt(0));
}

function json(part) {
  return JSON.parse(new TextDecoder().decode(bytes(part)));
}

/**
 * Returns { uid, email } for a valid token, or null. `options.keys` and
 * `options.now` (seconds) exist for tests.
 */
export async function verifyIdToken(token, options = {}) {
  try {
    const parts = String(token || "").split(".");
    if (parts.length !== 3) return null;
    const header = json(parts[0]);
    const claims = json(parts[1]);
    const now = options.now ?? Date.now() / 1000;
    const project = options.projectId || PROJECT_ID;
    if (header.alg !== "RS256" || !header.kid) return null;
    if (
      claims.iss !== `https://securetoken.google.com/${project}` ||
      claims.aud !== project
    )
      return null;
    if (
      typeof claims.sub !== "string" ||
      !claims.sub ||
      claims.sub.length > 128
    )
      return null;
    if (!(claims.exp > now) || !(claims.iat <= now + SKEW)) return null;
    if (claims.auth_time !== undefined && !(claims.auth_time <= now + SKEW))
      return null;
    const keys = options.keys || (await googleKeys());
    const jwk = keys.find((k) => k.kid === header.kid);
    if (!jwk) return null;
    const key = await crypto.subtle.importKey(
      "jwk",
      { kty: jwk.kty, n: jwk.n, e: jwk.e, alg: "RS256", ext: true },
      { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
      false,
      ["verify"],
    );
    const ok = await crypto.subtle.verify(
      "RSASSA-PKCS1-v1_5",
      key,
      bytes(parts[2]),
      new TextEncoder().encode(`${parts[0]}.${parts[1]}`),
    );
    return ok ? { uid: claims.sub, email: claims.email || "" } : null;
  } catch {
    return null;
  }
}
