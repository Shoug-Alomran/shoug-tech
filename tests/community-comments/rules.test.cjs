// Firestore rules for comments, profile colours and usernames (firebase/firestore.rules).
// A comment must carry its author's own profile name, and avatar colours must be
// plain hex because pages put them inside style attributes.
// Run (see firebase/README-course-transfers.md for the dependency install):
//   NODE_PATH=<deps>/node_modules firebase emulators:exec \
//     --project demo-shoug-comments --config firebase/firestore.emulator.json \
//     --only firestore 'node --test tests/community-comments/rules.test.cjs'
const { test, before, after, beforeEach } = require("node:test");
const fs = require("node:fs");
const path = require("node:path");
const {
  initializeTestEnvironment,
  assertSucceeds,
  assertFails,
} = require("@firebase/rules-unit-testing");
const testRequire = require("node:module").createRequire(
  require.resolve("@firebase/rules-unit-testing"),
);
const firebase = testRequire("firebase/compat/app");
testRequire("firebase/compat/firestore");
const now = () => firebase.firestore.FieldValue.serverTimestamp();

let env;
const as = (uid) => env.authenticatedContext(uid).firestore();
const profile = {
  username: "sara",
  displayName: "Sara",
  avatarColor: "#22c55e",
};
const comment = (extra = {}) => ({
  uid: "sara",
  username: "sara",
  displayName: "Sara",
  avatarColor: "#22c55e",
  avatarPreset: null,
  text: "Helpful page.",
  createdAt: now(),
  ...extra,
});
const pageComments = (db) =>
  db.collection("pageComments").doc("cs331").collection("comments");
const discussions = (db) =>
  db.collection("discussions").doc("cs331").collection("comments");

before(async () => {
  env = await initializeTestEnvironment({
    projectId: "demo-shoug-comments",
    firestore: {
      rules: fs.readFileSync(
        path.join(__dirname, "../../firebase/firestore.rules"),
        "utf8",
      ),
    },
  });
});
after(() => env.cleanup());
beforeEach(async () => {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled((ctx) =>
    ctx.firestore().collection("users").doc("sara").set(profile),
  );
});

test("a comment under your own profile name is accepted", async () => {
  await assertSucceeds(pageComments(as("sara")).add(comment()));
  await assertSucceeds(
    discussions(as("sara")).add(
      comment({ replyTo: "abc", replyToUsername: "noor" }),
    ),
  );
});

test("a comment posing as someone else is rejected", async () => {
  await assertFails(
    pageComments(as("sara")).add(comment({ username: "shoug" })),
  );
  await assertFails(
    pageComments(as("sara")).add(comment({ displayName: "Admin" })),
  );
  await assertFails(pageComments(as("sara")).add(comment({ uid: "noor" })));
});

test("a colour that could break out of a style attribute is rejected", async () => {
  const attack = '#fff" onmouseover="alert(1)';
  await assertFails(
    pageComments(as("sara")).add(comment({ avatarColor: attack })),
  );
  await assertFails(
    discussions(as("sara")).add(comment({ avatarColor: attack })),
  );
  await assertFails(
    as("sara")
      .collection("users")
      .doc("sara")
      .set({ ...profile, avatarColor: attack }),
  );
  await assertSucceeds(
    as("sara")
      .collection("users")
      .doc("sara")
      .set({ ...profile, avatarColor: "#b829ea" }),
  );
});

test("comments reject extra fields and empty or long text", async () => {
  await assertFails(pageComments(as("sara")).add(comment({ role: "admin" })));
  await assertFails(pageComments(as("sara")).add(comment({ text: "" })));
  await assertFails(
    pageComments(as("sara")).add(comment({ text: "x".repeat(1001) })),
  );
  await assertFails(
    pageComments(as("sara")).add(comment({ text: ["not", "text"] })),
  );
});

test("a signed-in student without a profile posts with empty names only", async () => {
  await assertSucceeds(
    pageComments(as("noor")).add(
      comment({ uid: "noor", username: "", displayName: "" }),
    ),
  );
  await assertFails(
    pageComments(as("noor")).add(comment({ uid: "noor", username: "sara" })),
  );
});

test("a username can only be claimed for yourself", async () => {
  await assertSucceeds(
    as("sara").collection("usernames").doc("sara").set({ uid: "sara" }),
  );
  await assertFails(
    as("noor").collection("usernames").doc("shoug").set({ uid: "sara" }),
  );
  await assertFails(
    as("noor")
      .collection("usernames")
      .doc("noor2")
      .set({ uid: "noor", extra: 1 }),
  );
});

test("signed-out visitors cannot comment", async () => {
  await assertFails(
    pageComments(env.unauthenticatedContext().firestore()).add(comment()),
  );
});

// Reply notifications: notifications/{toUid}/items/{id}.
const notif = (extra = {}) => ({
  type: "reply",
  fromUid: "sara",
  fromUsername: "sara",
  fromDisplayName: "Sara",
  fromAvatarColor: "#22c55e",
  pageUrl: "/academics/computer-science/cs331/",
  commentPreview: "Thanks, that helped.",
  read: false,
  createdAt: now(),
  ...extra,
});
const inbox = (db, uid) =>
  db.collection("notifications").doc(uid).collection("items");

test("a reply notification to another student is delivered", async () => {
  await assertSucceeds(inbox(as("sara"), "noor").add(notif()));
});

test("notifications can't impersonate, link off-site or notify yourself", async () => {
  await assertFails(inbox(as("sara"), "noor").add(notif({ fromUid: "shoug" })));
  await assertFails(
    inbox(as("sara"), "noor").add(notif({ fromDisplayName: "Admin" })),
  );
  await assertFails(
    inbox(as("sara"), "noor").add(notif({ pageUrl: "javascript:alert(1)" })),
  );
  await assertFails(
    inbox(as("sara"), "noor").add(notif({ pageUrl: "//evil.example/" })),
  );
  await assertFails(
    inbox(as("sara"), "noor").add(notif({ pageUrl: "https://evil.example/" })),
  );
  await assertFails(inbox(as("sara"), "noor").add(notif({ read: true })));
  await assertFails(inbox(as("sara"), "noor").add(notif({ extra: 1 })));
  await assertFails(inbox(as("sara"), "sara").add(notif()));
  await assertFails(
    inbox(env.unauthenticatedContext().firestore(), "noor").add(notif()),
  );
});

test("only the recipient reads, marks read and deletes", async () => {
  const ref = await inbox(as("sara"), "noor").add(notif());
  const id = ref.id;
  await assertFails(inbox(as("sara"), "noor").doc(id).get());
  await assertSucceeds(
    inbox(as("noor"), "noor").where("read", "==", false).limit(20).get(),
  );
  await assertFails(
    inbox(as("noor"), "noor").doc(id).update({ commentPreview: "edited" }),
  );
  await assertSucceeds(
    inbox(as("noor"), "noor").doc(id).update({ read: true }),
  );
  await assertFails(inbox(as("sara"), "noor").doc(id).delete());
  await assertSucceeds(inbox(as("noor"), "noor").doc(id).delete());
});

// Planner, bookmark and degree-plan data is private: never on the public profile.
test("study and bookmark data can't be put on the public profile", async () => {
  const me = as("sara").collection("users").doc("sara");
  for (const field of [
    "studyPlannerChat",
    "studyAvailability",
    "studyPlan",
    "degreePlan",
    "academicPlanGrids",
    "bookmarkFolders",
  ]) {
    await assertFails(me.set({ [field]: { x: 1 } }, { merge: true }));
  }
  await assertSucceeds(
    me
      .collection("private")
      .doc("data")
      .set(
        {
          bookmarkFolders: [{ name: "Exams" }],
          studyPlannerChat: [{ q: "hi" }],
        },
        { merge: true },
      ),
  );
  await assertFails(
    as("noor")
      .collection("users")
      .doc("sara")
      .collection("private")
      .doc("data")
      .get(),
  );
});

test("an old profile copy of private data can be removed", async () => {
  await env.withSecurityRulesDisabled((ctx) =>
    ctx
      .firestore()
      .collection("users")
      .doc("sara")
      .set({ ...profile, bookmarkFolders: ["old"] }),
  );
  await assertSucceeds(
    as("sara").collection("users").doc("sara").update({
      bookmarkFolders: firebase.firestore.FieldValue.delete(),
    }),
  );
});
