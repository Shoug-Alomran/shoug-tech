const { test } = require("node:test");
const assert = require("node:assert/strict");
const { JSDOM } = require("jsdom");
const fs = require("node:fs");
const path = require("node:path");
const script = fs.readFileSync(
  path.join(__dirname, "../../docs/javascripts/email-verification.js"),
  "utf8",
);
const flush = async () => {
  for (let i = 0; i < 5; i++)
    await new Promise((resolve) => setImmediate(resolve));
};
function setup(t) {
  const dom = new JSDOM("", {
    runScripts: "outside-only",
    pretendToBeVisual: true,
    url: "https://shoug-tech.com/checkout/ethics/",
  });
  t.after(() => dom.window.close());
  dom.window.eval(script);
  return dom.window;
}
test("already-used link with a now-verified account continues without sending another email", async (t) => {
  const w = setup(t);
  let sent = 0,
    continued = 0,
    refreshed = 0;
  const user = {
    uid: "a",
    email: "a@example.test",
    emailVerified: false,
    reload: async () => {
      user.emailVerified = true;
    },
    getIdToken: async (force) => {
      assert.equal(force, true);
      refreshed++;
    },
    sendEmailVerification: async () => {
      sent++;
    },
  };
  w.ShougEmailVerification.start({
    user,
    isCurrent: () => true,
    onVerified: () => {
      continued++;
    },
    onStatus() {},
  });
  await flush();
  assert.equal(sent, 0);
  assert.equal(continued, 1);
  assert.equal(refreshed, 1);
});
test("automatic sends are deduplicated across repeated visits and manual resends are throttled", async (t) => {
  const w = setup(t);
  let sent = 0;
  const user = {
    uid: "a",
    email: "a@example.test",
    emailVerified: false,
    reload: async () => {},
    sendEmailVerification: async () => {
      sent++;
    },
  };
  const options = {
    user,
    isCurrent: () => true,
    onVerified() {},
    onStatus() {},
  };
  const first = w.ShougEmailVerification.start(options);
  await flush();
  first.stop();
  const next = w.ShougEmailVerification.start(options);
  await flush();
  await next.resend();
  assert.equal(sent, 1);
});
test("an expired-link recovery can send a fresh link after the cooldown", async (t) => {
  const w = setup(t);
  let sent = 0;
  w.localStorage.setItem(
    "shoug-verification-sent:a",
    String(Date.now() - 61000),
  );
  const user = {
    uid: "a",
    email: "a@example.test",
    emailVerified: false,
    reload: async () => {},
    sendEmailVerification: async () => {
      sent++;
    },
  };
  const controller = w.ShougEmailVerification.start({
    user,
    isCurrent: () => true,
    onVerified() {},
    onStatus() {},
  });
  await flush();
  assert.equal(sent, 0);
  await controller.resend();
  assert.equal(sent, 1);
});
test("changing accounts cancels the previous account verification watcher", async (t) => {
  const w = setup(t);
  let current = true,
    continued = 0,
    release;
  const user = {
    uid: "a",
    email: "a@example.test",
    emailVerified: false,
    reload: () =>
      new Promise((resolve) => {
        release = resolve;
      }),
    getIdToken: async () => {},
    sendEmailVerification: async () => {
      throw new Error("must not send");
    },
  };
  const controller = w.ShougEmailVerification.start({
    user,
    isCurrent: () => current,
    onVerified: () => {
      continued++;
    },
    onStatus() {},
  });
  current = false;
  controller.stop();
  user.emailVerified = true;
  release();
  await flush();
  assert.equal(continued, 0);
});
test("email provider throttling shows recovery instead of retrying repeatedly", async (t) => {
  const w = setup(t);
  let sent = 0,
    status = "";
  const user = {
    uid: "a",
    email: "a@example.test",
    emailVerified: false,
    reload: async () => {},
    sendEmailVerification: async () => {
      sent++;
      throw { code: "auth/too-many-requests" };
    },
  };
  w.ShougEmailVerification.start({
    user,
    isCurrent: () => true,
    onVerified() {},
    onStatus: (value) => {
      status = value;
    },
  });
  await flush();
  assert.equal(sent, 1);
  assert.match(status, /latest link/);
});
