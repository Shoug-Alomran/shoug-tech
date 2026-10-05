const ROOT = "/academics/other-courses/ethcs303";
const COOKIE = "__Host-ethics_session";
export function protectedPath(path) {
  return (
    path === ROOT ||
    path.startsWith(ROOT + "/") ||
    path.startsWith("/course-media/ethics/") ||
    path === "/javascripts/past-exam-practice.js" ||
    path === "/ai-context" + ROOT ||
    path.startsWith("/ai-context" + ROOT + "/")
  );
}
function privateResponse(body, status = 200, headers = {}) {
  return new Response(body, {
    status,
    headers: {
      "Cache-Control": "private, no-store, max-age=0",
      Vary: "Cookie, Authorization",
      "X-Content-Type-Options": "nosniff",
      "X-Robots-Tag": "noindex, noarchive",
      "Referrer-Policy": "same-origin",
      ...headers,
    },
  });
}
function json(body, status = 200, headers = {}) {
  return privateResponse(JSON.stringify(body), status, {
    "Content-Type": "application/json",
    ...headers,
  });
}
export async function authorize(token, env, fetcher = fetch) {
  if (!token || token.length > 12000) return { allowed: false, status: 401 };
  // Firebase validates the actual ID token. No browser-provided email, role,
  // payment status, localStorage flag, or unsigned JWT payload is trusted.
  const identity = await fetcher(
    "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" +
      env.FIREBASE_API_KEY,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Referer: "https://shoug-tech.com/",
      },
      body: JSON.stringify({ idToken: token }),
    },
  );
  if (!identity.ok)
    return { allowed: false, status: identity.status >= 500 ? 503 : 401 };
  const account = (await identity.json()).users?.[0];
  if (!account?.localId || !account.emailVerified || account.disabled)
    return { allowed: false, status: 401 };
  const base = `https://firestore.googleapis.com/v1/projects/${env.FIREBASE_PROJECT}/databases/(default)/documents/`;
  const headers = { Authorization: "Bearer " + token };
  const config = await fetcher(
    base + "courseCommerce/ethics?mask.fieldPaths=adminUid",
    { headers },
  );
  if (
    config.ok &&
    (await config.json()).fields?.adminUid?.stringValue === account.localId
  )
    return { allowed: true };
  const order = await fetcher(
    base +
      "courseTransfers/" +
      encodeURIComponent(account.localId) +
      "?mask.fieldPaths=status&mask.fieldPaths=course&mask.fieldPaths=amount&mask.fieldPaths=currency",
    { headers },
  );
  if (!order.ok)
    return { allowed: false, status: order.status >= 500 ? 503 : 403 };
  const fields = (await order.json()).fields;
  return fields?.status?.stringValue === "approved" &&
    fields?.course?.stringValue === "ethics" &&
    fields?.amount?.integerValue === "32500" &&
    fields?.currency?.stringValue === "SAR"
    ? { allowed: true }
    : { allowed: false, status: 403 };
}
export function parseRange(value, size) {
  const match = /^bytes=(\d*)-(\d*)$/.exec(value);
  if (!match || (!match[1] && !match[2])) return null;
  let start, end;
  if (!match[1]) {
    const suffix = Number(match[2]);
    if (!Number.isSafeInteger(suffix) || suffix <= 0) return null;
    start = Math.max(0, size - suffix);
    end = size - 1;
  } else {
    start = Number(match[1]);
    end = match[2] ? Math.min(Number(match[2]), size - 1) : size - 1;
  }
  if (
    !Number.isSafeInteger(start) ||
    !Number.isSafeInteger(end) ||
    start >= size ||
    start > end
  )
    return null;
  return { offset: start, length: end - start + 1 };
}
async function gate(env, status = 200) {
  const response = await env.ASSETS.fetch(
    new Request("https://assets.invalid/course-access/index.html"),
  );
  return privateResponse(response.body, status, {
    "Content-Type": "text/html; charset=utf-8",
  });
}
async function serveVideo(request, env, key) {
  const metadata = await env.VIDEOS.head(key);
  if (!metadata) return json({ error: "Not found" }, 404);
  const rangeHeader = request.headers.get("Range"),
    range = rangeHeader ? parseRange(rangeHeader, metadata.size) : undefined;
  if (rangeHeader && !range)
    return privateResponse(null, 416, {
      "Content-Range": "bytes */" + metadata.size,
    });
  const headers = {
    "Content-Type": metadata.httpMetadata?.contentType || "video/mp4",
    "Accept-Ranges": "bytes",
    "Content-Length": String(range?.length ?? metadata.size),
  };
  if (range)
    headers["Content-Range"] =
      `bytes ${range.offset}-${range.offset + range.length - 1}/${metadata.size}`;
  const object =
    request.method === "HEAD"
      ? null
      : await env.VIDEOS.get(key, range ? { range } : {});
  if (request.method !== "HEAD" && !object)
    return json({ error: "Not found" }, 404);
  return privateResponse(object?.body || null, range ? 206 : 200, headers);
}
export async function handle(request, env, fetcher = fetch) {
  const url = new URL(request.url);
  let path;
  try {
    path = decodeURIComponent(url.pathname);
  } catch {
    return json({ error: "Invalid path" }, 400);
  }
  if (
    path.includes("\\") ||
    path.split("/").some((part) => part === ".." || part === ".")
  )
    return json({ error: "Invalid path" }, 400);
  if (path.startsWith("/course-access/samples/")) {
    if (!["GET", "HEAD"].includes(request.method))
      return json({ error: "Method not allowed" }, 405);
    if (path === "/course-access/samples/intro-video.mp4") {
      return serveVideo(
        request,
        env,
        "ethics/Moral Systems, Ethical Concepts, and Theories/Divine Command Theory.mp4",
      );
    }
    return env.ASSETS.fetch(request);
  }
  const publicFiles = [
    "/checkout/ethics",
    "/checkout/ethics/",
    "/checkout/ethics/index.html",
    "/admin/transfers",
    "/admin/transfers/",
    "/admin/transfers/index.html",
    "/styles/course-transfers.css",
    "/javascripts/course-transfers.js",
    "/javascripts/email-verification.js",
    "/javascripts/firebase-auth.js",
    "/sw.js",
    "/styles/site-shell.css",
    "/javascripts/site-shell.js",
    "/javascripts/mobile-navigation.js",
    "/styles/ethics-study-tools.css",
    "/javascripts/ethics-study-tools.js",
  ];
  if (publicFiles.includes(path)) {
    const asset = await env.ASSETS.fetch(request);
    return privateResponse(
      asset.body,
      asset.status,
      Object.fromEntries(
        [...asset.headers].filter(
          ([key]) => !["cache-control", "vary"].includes(key.toLowerCase()),
        ),
      ),
    );
  }
  if (["/search-index.json", "/search-pdf-index.json"].includes(path)) {
    try {
      const upstream = await fetcher(request);
      if (!upstream.ok) return json([], 503);
      const rows = await upstream.json();
      if (!Array.isArray(rows)) return json([], 503);
      return json(
        rows.filter(
          (row) =>
            !["url", "u", "f", "path"].some((key) =>
              String(row[key] || "").includes(ROOT),
            ),
        ),
      );
    } catch {
      return json([], 503);
    }
  }
  if (
    ["/course-access/gate.js", "/course-access/session-sync.js"].includes(path)
  )
    return env.ASSETS.fetch(request);
  if (
    path === "/course-access" ||
    path === "/course-access/" ||
    path === "/course-access/index.html"
  )
    return gate(env);
  if (path === "/course-access/session") {
    if (!["POST", "DELETE"].includes(request.method))
      return json({ error: "Method not allowed" }, 405);
    if (request.headers.get("Origin") !== url.origin)
      return json({ error: "Invalid origin" }, 403);
    if (request.method === "DELETE")
      return json({ cleared: true }, 200, {
        "Set-Cookie":
          COOKIE + "=; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=0",
      });
    try {
      const body = await request.text();
      if (body.length > 16000) return json({ error: "Request too large" }, 413);
      const { idToken } = JSON.parse(body);
      if (typeof idToken !== "string" || /[\s;]/.test(idToken))
        return json({ error: "Invalid token" }, 400);
      const result = await authorize(idToken, env, fetcher);
      if (!result.allowed)
        return json(
          {
            error:
              result.status === 403
                ? "Payment approval required"
                : "Unable to verify access",
          },
          result.status,
        );
      return json({ approved: true }, 200, {
        "Set-Cookie":
          COOKIE +
          "=" +
          idToken +
          "; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=3600",
      });
    } catch {
      return json({ error: "Unable to verify access" }, 503);
    }
  }
  if (!protectedPath(path)) return json({ error: "Not found" }, 404);
  if (!["GET", "HEAD"].includes(request.method))
    return json({ error: "Method not allowed" }, 405);
  const token =
    request.headers.get("Authorization")?.replace(/^Bearer /, "") ||
    request.headers
      .get("Cookie")
      ?.split(";")
      .map((v) => v.trim())
      .find((v) => v.startsWith(COOKIE + "="))
      ?.slice(COOKIE.length + 1);
  try {
    const access = await authorize(token, env, fetcher);
    if (!access.allowed) {
      const navigation =
        request.headers.get("Sec-Fetch-Dest") === "document" ||
        request.headers.get("Accept")?.includes("text/html") ||
        path.endsWith("/") ||
        path.endsWith(".html") ||
        path === ROOT;
      return navigation
        ? gate(env, access.status === 503 ? 503 : 200)
        : json({ error: "Approved course purchase required" }, access.status);
    }
    if (path.startsWith("/course-media/ethics/")) {
      const key = path.slice("/course-media/".length);
      return serveVideo(request, env, key);
    }
    const response = await env.ASSETS.fetch(request);
    return privateResponse(
      request.method === "HEAD" ? null : response.body,
      response.status,
      Object.fromEntries(
        [...response.headers].filter(
          ([key]) => !["cache-control", "vary"].includes(key.toLowerCase()),
        ),
      ),
    );
  } catch {
    return json({ error: "Course access is temporarily unavailable" }, 503);
  }
}
export default {
  fetch(request, env) {
    return handle(request, env);
  },
};
