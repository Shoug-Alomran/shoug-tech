const { test, before, after, beforeEach } = require("node:test");
const fs = require("node:fs");
const path = require("node:path");
const {
  initializeTestEnvironment,
  assertSucceeds,
  assertFails,
} = require("@firebase/rules-unit-testing");
// Resolve the same SDK instance as the test environment, even if an ancestor
// workspace has a different Firebase version installed.
const testRequire = require("node:module").createRequire(
  require.resolve("@firebase/rules-unit-testing"),
);
const firebase = testRequire("firebase/compat/app");
testRequire("firebase/compat/firestore");
const doc = (db, ...parts) => db.doc(parts.join("/"));
const setDoc = (ref, data) => ref.set(data);
const getDoc = (ref) => ref.get();
const updateDoc = (ref, data) => ref.update(data);
const deleteDoc = (ref) => ref.delete();
const collection = (db, name) => db.collection(name);
const getDocs = (ref) => ref.get();
const limit = (size) => size;
const query = (ref, size) => ref.limit(size);
const serverTimestamp = () => firebase.firestore.FieldValue.serverTimestamp();
let env;
const config = {
  enabled: true,
  adminUid: "admin",
  bankName: "Test Bank",
  beneficiary: "Test Owner",
  iban: "SA0000000000000000000000",
};
const auth = (uid, verified = true) =>
  env
    .authenticatedContext(uid, {
      email: uid + "@example.com",
      email_verified: verified,
    })
    .firestore();
const order = (uid, overrides = {}) => ({
  uid,
  email: uid + "@example.com",
  fullName: "Test Buyer",
  phone: "+966531007472",
  course: "ethics",
  amount: 32500,
  currency: "SAR",
  status: "pending",
  receipt: "data:image/jpeg;base64,/9j/AA==",
  submittedAt: serverTimestamp(),
  reviewedAt: null,
  reviewedBy: "",
  reviewNote: "",
  ...overrides,
});
const ref = (db, uid = "buyer") => doc(db, "courseTransfers", uid);
const review = (status, overrides = {}) => ({
  status,
  reviewedAt: serverTimestamp(),
  reviewedBy: "admin",
  reviewNote: "",
  ...overrides,
});
before(async () => {
  env = await initializeTestEnvironment({
    projectId: "demo-shoug-transfers",
    firestore: {
      host: "127.0.0.1",
      port: 8088,
      rules: fs.readFileSync(
        path.join(__dirname, "../../firebase/course-transfers.rules"),
        "utf8",
      ),
    },
  });
});
beforeEach(async () => {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async (ctx) =>
    setDoc(doc(ctx.firestore(), "courseCommerce", "ethics"), config),
  );
});
after(async () => {
  if (env) await env.cleanup();
});
test("requires verified login, account-owned email and exact course price", async () => {
  await assertFails(
    setDoc(ref(env.unauthenticatedContext().firestore()), order("buyer")),
  );
  await assertFails(setDoc(ref(auth("buyer", false)), order("buyer")));
  await assertFails(
    setDoc(
      ref(auth("buyer")),
      order("buyer", { email: "someone@example.com" }),
    ),
  );
  await assertFails(setDoc(ref(auth("buyer")), order("buyer", { amount: 1 })));
  await assertFails(
    setDoc(ref(auth("buyer")), order("buyer", { status: "approved" })),
  );
  await assertFails(
    setDoc(ref(auth("buyer")), order("buyer", { extra: true })),
  );
  await assertSucceeds(setDoc(ref(auth("buyer")), order("buyer")));
});
test("receipts cannot be external links, HTML, or oversized payloads", async () => {
  for (const receipt of [
    "https://example.com/receipt.jpg",
    "data:image/svg+xml,<svg/>",
    "data:image/jpeg;base64," + "A".repeat(700001),
  ]) {
    await assertFails(setDoc(ref(auth("buyer")), order("buyer", { receipt })));
  }
});
test("only the buyer and administrator can read proof; listing is bounded and admin-only", async () => {
  await setDoc(ref(auth("buyer")), order("buyer"));
  await assertSucceeds(getDoc(ref(auth("buyer"))));
  await assertSucceeds(getDoc(ref(auth("admin"))));
  await assertFails(getDoc(ref(auth("other"))));
  await assertFails(getDoc(ref(env.unauthenticatedContext().firestore())));
  await assertFails(
    getDocs(query(collection(auth("buyer"), "courseTransfers"), limit(10))),
  );
  await assertSucceeds(
    getDocs(query(collection(auth("admin"), "courseTransfers"), limit(10))),
  );
  await assertFails(getDocs(collection(auth("admin"), "courseTransfers")));
  await assertFails(
    getDocs(query(collection(auth("admin"), "courseTransfers"), limit(11))),
  );
});
test("buyers cannot self-approve, overwrite pending proof, change config, or delete records", async () => {
  const buyer = auth("buyer");
  await setDoc(ref(buyer), order("buyer"));
  await assertFails(
    updateDoc(ref(buyer), review("approved", { reviewedBy: "buyer" })),
  );
  await assertFails(setDoc(ref(buyer), order("buyer")));
  await assertFails(deleteDoc(ref(buyer)));
  await assertFails(
    updateDoc(doc(buyer, "courseCommerce", "ethics"), { adminUid: "buyer" }),
  );
  await assertFails(
    updateDoc(doc(auth("admin"), "courseCommerce", "ethics"), {
      adminUid: "buyer",
    }),
  );
});
test("admin can approve pending payment but cannot alter evidence or re-review it", async () => {
  await setDoc(ref(auth("buyer")), order("buyer"));
  await assertFails(
    updateDoc(
      ref(auth("admin")),
      review("approved", { email: "changed@example.com" }),
    ),
  );
  await assertFails(
    updateDoc(
      ref(auth("admin")),
      review("approved", { receipt: "data:image/jpeg;base64,AA==" }),
    ),
  );
  await assertFails(updateDoc(ref(auth("other")), review("approved")));
  await assertSucceeds(updateDoc(ref(auth("admin")), review("approved")));
  await assertFails(updateDoc(ref(auth("admin")), review("rejected")));
  await assertFails(setDoc(ref(auth("buyer")), order("buyer")));
});
test("rejected buyers can resubmit proof, resetting review fields", async () => {
  await setDoc(ref(auth("buyer")), order("buyer"));
  await assertSucceeds(
    updateDoc(
      ref(auth("admin")),
      review("rejected", { reviewNote: "Please upload a readable receipt." }),
    ),
  );
  await assertFails(setDoc(ref(auth("other")), order("other")));
  await assertSucceeds(setDoc(ref(auth("buyer")), order("buyer")));
  await assertSucceeds(updateDoc(ref(auth("admin")), review("approved")));
});
test("checkout is fail-closed when disabled or unconfigured", async () => {
  await env.withSecurityRulesDisabled(async (ctx) =>
    updateDoc(doc(ctx.firestore(), "courseCommerce", "ethics"), {
      enabled: false,
    }),
  );
  await assertFails(setDoc(ref(auth("buyer")), order("buyer")));
  await env.withSecurityRulesDisabled(async (ctx) =>
    deleteDoc(doc(ctx.firestore(), "courseCommerce", "ethics")),
  );
  await assertFails(setDoc(ref(auth("buyer")), order("buyer")));
});

test("registration requires a name and international phone", async () => {
  for (const fields of [
    { fullName: "" },
    { fullName: "   " },
    { phone: "123" },
    { phone: "+000000000" },
  ]) {
    await assertFails(setDoc(ref(auth("buyer")), order("buyer", fields)));
  }
});
