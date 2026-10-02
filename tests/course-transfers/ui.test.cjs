const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");
const root = path.join(__dirname, "../..");
const script = fs.readFileSync(
  path.join(root, "docs/javascripts/course-transfers.js"),
  "utf8",
);
const flush = async () => {
  for (let i = 0; i < 5; i++)
    await new Promise((resolve) => setImmediate(resolve));
};

async function fixture(
  t,
  {
    page = "checkout",
    signedIn = true,
    verified = true,
    configured = true,
    order = null,
  } = {},
) {
  const html = fs.readFileSync(
    path.join(
      root,
      page === "admin"
        ? "docs/admin/transfers/index.html"
        : "docs/checkout/ethics/index.html",
    ),
    "utf8",
  );
  const dom = new JSDOM(html, {
    runScripts: "outside-only",
    pretendToBeVisual: true,
    url: "https://example.test/",
  });
  t.after(() => dom.window.close());
  const w = dom.window,
    $ = (id) => w.document.getElementById(id);
  let verificationEmails = 0;
  const user = signedIn
    ? {
        uid: page === "admin" ? "admin" : "buyer",
        email: "buyer@example.com",
        emailVerified: verified,
        reload: async () => {},
        getIdToken: async () => "refreshed-token",
        sendEmailVerification: async () => {
          verificationEmails++;
        },
      }
    : null;
  let authListener,
    listener,
    saved,
    current = order,
    reads = 0;
  const snapshot = () => ({
    exists: !!current,
    data: () => current,
    id: "buyer",
    ref,
  });
  const ref = {
    get: async () => snapshot(),
    onSnapshot(callback) {
      listener = callback;
      callback(snapshot());
      return () => {
        listener = null;
      };
    },
  };
  const filters = {};
  const query = {
    where(field, op, value) { filters[field] = value; return this; },
    startAfter() { return this; },
    orderBy() {
      return this;
    },
    limit() {
      return this;
    },
    get: async () => ({
      docs: current && Object.entries(filters).every(([key,value]) => current[key] === value) ? [snapshot()] : [],
      size: current ? 1 : 0,
      empty: !current,
    }),
  };
  const db = {
    collection(name) {
      Object.keys(filters).forEach(key => delete filters[key]);
      reads++;
      return name === "courseCommerce"
        ? {
            doc: () => ({
              get: async () => ({
                exists: configured,
                data: () => ({
                  enabled: true,
                  adminUid: "admin",
                  bankName: "Test Bank",
                  beneficiary: "Test Owner",
                  iban: "SA0000000000000000000000",
                }),
              }),
            }),
          }
        : { ...query, doc: () => ref };
    },
    async runTransaction(fn) {
      await fn({
        get: async () => snapshot(),
        set(_, data) {
          saved = data;
          current = data;
        },
        update(_, data) {
          saved = data;
          current = { ...current, ...data };
        },
      });
      if (listener) listener(snapshot());
    },
  };
  const auth = {
    currentUser: user,
    onAuthStateChanged(callback) {
      authListener = callback;
      callback(user);
    },
  };
  const firestore = () => db;
  firestore.FieldValue = { serverTimestamp: () => "SERVER_TIMESTAMP" };
  w.__shoug_fb = { auth: () => auth, firestore };
  w.createImageBitmap = async () => ({ width: 800, height: 1200, close() {} });
  w.HTMLCanvasElement.prototype.getContext = () => ({
    fillRect() {},
    drawImage() {},
  });
  w.HTMLCanvasElement.prototype.toDataURL = () =>
    "data:image/jpeg;base64,/9j/AA==";
  w.eval(
    fs.readFileSync(
      path.join(root, "docs/javascripts/email-verification.js"),
      "utf8",
    ),
  );
  w.eval(script);
  await flush();
  return {
    w,
    $,
    user,
    verificationEmails: () => verificationEmails,
    saved: () => saved,
    reads: () => reads,
    signOut: async () => {
      auth.currentUser = null;
      authListener(null);
      await flush();
    },
  };
}

test("signed-out and unverified buyers cannot see payment instructions or upload form", async (t) => {
  for (const options of [{ signedIn: false }, { verified: false }]) {
    const f = await fixture(t, options);
    assert.equal(f.$("transfer-bank").hidden, true);
    assert.equal(f.$("transfer-form").hidden, true);
    assert.equal(f.reads(), 0);
  }
});
test("missing bank configuration keeps checkout closed", async (t) => {
  const f = await fixture(t, { configured: false });
  assert.equal(f.$("transfer-form").hidden, true);
  assert.match(f.$("transfer-message").textContent, /not open yet/);
});
test("verification sends automatically and checkout resumes on return from email", async (t) => {
  const f = await fixture(t, { verified: false });
  assert.equal(f.verificationEmails(), 1);
  assert.equal(f.$("transfer-refresh"), null);
  assert.equal(f.$("transfer-verify").hidden, false);
  f.user.emailVerified = true;
  f.w.dispatchEvent(new f.w.Event("focus"));
  await flush();
  assert.equal(f.$("transfer-verify").hidden, true);
  assert.equal(f.$("transfer-bank").hidden, false);
  assert.equal(f.verificationEmails(), 1);
});
test("receipt is required and a valid upload is tied to authenticated email as pending", async (t) => {
  const f = await fixture(t),
    { w, $ } = f;
  $("transfer-form").dispatchEvent(new w.Event("submit", { cancelable: true }));
  await flush();
  assert.equal(f.saved(), undefined);
  Object.defineProperty($("transfer-photo"), "files", {
    value: [{ type: "image/png", size: 1024 }],
  });
  $("transfer-photo").dispatchEvent(new w.Event("change"));
  await flush();
  assert.equal($("transfer-preview").hidden, false);
  $("transfer-name").value = "Test Buyer";
  $("transfer-phone").value = "0531007472";
  $("transfer-consent").checked = true;
  $("transfer-form").dispatchEvent(new w.Event("submit", { cancelable: true }));
  await flush();
  assert.equal(f.saved().email, "buyer@example.com");
  assert.equal(f.saved().uid, "buyer");
  assert.equal(f.saved().fullName, "Test Buyer");
  assert.equal(f.saved().phone, "+966531007472");
  assert.equal(f.saved().status, "pending");
  assert.equal(f.saved().amount, 32500);
  assert.equal($("transfer-form").hidden, true);
  await f.signOut();
  assert.equal($("transfer-preview").hasAttribute("src"), false);
  assert.equal($("transfer-login").hidden, false);
});
test("pending purchases cannot submit again; rejected purchases can correct proof", async (t) => {
  for (const status of ["pending", "approved", "rejected"]) {
    const f = await fixture(t, {
      order: { status, reviewNote: "Upload readable proof." },
    });
    assert.equal(f.$("transfer-form").hidden, status !== "rejected");
  }
});
test("admin sees email and proof together; approval needs explicit bank verification", async (t) => {
  const f = await fixture(t, {
    page: "admin",
    order: {
      uid: "buyer",
      email: "buyer@example.com",
      status: "pending",
      receipt: "data:image/jpeg;base64,/9j/AA==",
      submittedAt: { toDate: () => new Date() },
    },
  });
  const list = f.$("transfer-orders");
  assert.match(list.textContent, /buyer@example.com/);
  assert.equal(list.querySelectorAll("img.receipt").length, 1);
  const approve = [...list.querySelectorAll("button")].find(
    (button) => button.textContent === "Approve payment",
  );
  assert.equal(approve.disabled, true);
  const check = list.querySelector("input[type=checkbox]");
  check.checked = true;
  check.dispatchEvent(new f.w.Event("change"));
  approve.click();
  await flush();
  assert.equal(f.saved().status, "approved");
  assert.equal(f.saved().reviewedBy, "admin");
  await f.signOut();
  assert.equal(list.children.length, 0);
});

 test("admin status tabs query the selected status and email", async t => {
 const f = await fixture(t, {page:"admin", order:{uid:"buyer",email:"buyer@example.com",status:"approved",receipt:"data:image/jpeg;base64,/9j/AA=="}});
 assert.equal(f.$("transfer-orders").children.length,0);
 f.w.document.querySelector('[data-status="approved"]').click(); await flush();
 assert.match(f.$("transfer-orders").textContent,/buyer@example.com/);
 assert.equal(f.w.document.querySelector('[data-status="approved"]').getAttribute("aria-pressed"),"true");
 f.$("review-email").value="absent@example.com"; f.$("review-search").dispatchEvent(new f.w.Event("submit",{cancelable:true})); await flush();
 assert.equal(f.$("transfer-orders").children.length,0);
 f.$("review-clear").click(); await flush();
 f.w.document.querySelector('[data-status="all"]').click(); await flush();
 assert.match(f.$("transfer-orders").textContent,/buyer@example.com/);
 });
