// Firestore rules for private student data (firebase/firestore.rules):
// users/{uid} is a public profile, users/{uid}/private/data is owner-only.
// Run (see firebase/README-course-transfers.md for the dependency install):
//   NODE_PATH=<deps>/node_modules <deps>/node_modules/.bin/firebase emulators:exec \
//     --project demo-shoug-private --config firebase/firestore.emulator.json \
//     --only firestore 'node --test tests/private-record/rules.test.cjs'
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
const del = () => firebase.firestore.FieldValue.delete();

let env;
const as = (uid) => env.authenticatedContext(uid).firestore();
const record = {
  academicRecord: {
    courses: {
      "CS 331": { letter: "A", hours: 3, term: "252", finished: true },
    },
    transcript: { gpa: 3, hours: 76, term: "253" },
  },
  calendarGrades: [
    { id: "g1", course: "SE 322", earned: 9, possible: 10, weight: 10 },
  ],
  exams: { e1: { course: "SE423", date: "2026-11-01" } },
};

before(async () => {
  env = await initializeTestEnvironment({
    projectId: "demo-shoug-private",
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
  await env.withSecurityRulesDisabled(async (ctx) => {
    const db = ctx.firestore();
    await db.doc("users/shoug").set({ username: "shoug", major: "SE" });
    await db.doc("users/shoug/private/data").set(record);
    // An account from before the move, still holding private fields.
    await db.doc("users/legacy").set({ username: "legacy", ...record });
  });
});

test("only the owner can read the private record", async () => {
  await assertSucceeds(as("shoug").doc("users/shoug/private/data").get());
  await assertFails(as("someone").doc("users/shoug/private/data").get());
  await assertFails(
    env
      .unauthenticatedContext()
      .firestore()
      .doc("users/shoug/private/data")
      .get(),
  );
});

test("public profiles stay readable to signed-in students", async () => {
  await assertSucceeds(as("someone").doc("users/shoug").get());
});

test("only the owner can write the private record, and only the data doc", async () => {
  await assertSucceeds(
    as("shoug")
      .doc("users/shoug/private/data")
      .set({ calendarEvents: [] }, { merge: true }),
  );
  await assertFails(
    as("someone")
      .doc("users/shoug/private/data")
      .set({ calendarEvents: [] }, { merge: true }),
  );
  await assertFails(as("shoug").doc("users/shoug/private/other").set({ x: 1 }));
});

test("the private record still validates transcript totals", async () => {
  const db = as("shoug");
  await assertFails(
    db
      .doc("users/shoug/private/data")
      .set(
        { academicRecord: { transcript: { gpa: 9, hours: 76, term: "253" } } },
        { merge: true },
      ),
  );
  await assertFails(
    db
      .doc("users/shoug/private/data")
      .set({ academicRecord: { other: 1 } }, { merge: true }),
  );
});

test("private fields can no longer be written to the public profile", async () => {
  const db = as("shoug");
  await assertFails(
    db
      .doc("users/shoug")
      .set({ academicRecord: record.academicRecord }, { merge: true }),
  );
  await assertFails(db.doc("users/shoug").set({ exams: {} }, { merge: true }));
  await assertSucceeds(
    db.doc("users/shoug").set({ bio: "hi" }, { merge: true }),
  );
  await assertFails(
    as("newbie")
      .doc("users/newbie")
      .set({ username: "newbie", calendarEvents: [] }),
  );
  await assertSucceeds(
    as("newbie").doc("users/newbie").set({ username: "newbie" }),
  );
});

test("an older profile can still be edited, and the one-time move is allowed", async () => {
  const db = as("legacy");
  // Editing the profile without touching private fields works before the move.
  await assertSucceeds(db.doc("users/legacy").update({ bio: "still works" }));
  // Changing a private field on the profile does not.
  await assertFails(
    db.doc("users/legacy").update({ "academicRecord.transcript.gpa": 4 }),
  );
  // The move: copy to the private record, then delete every private field at once.
  await assertSucceeds(
    db.doc("users/legacy/private/data").set(record, { merge: true }),
  );
  const drop = {};
  ["academicRecord", "calendarGrades", "exams"].forEach(
    (k) => (drop[k] = del()),
  );
  await assertSucceeds(db.doc("users/legacy").update(drop));
});
