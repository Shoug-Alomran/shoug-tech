// Firestore rules for resource thumbs up/down (firebase/firestore.rules).
// Run (see firebase/README-course-transfers.md for the dependency install):
//   NODE_PATH=<deps>/node_modules <deps>/node_modules/.bin/firebase emulators:exec \
//     --project demo-shoug-resources --config firebase/firestore.emulator.json \
//     --only firestore 'node --test tests/resource-ratings/rules.test.cjs'
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
const { FieldValue } = firebase.firestore;

const PATH = "/academics/software-engineering/se423/slides/chapter-1/";
const ID = PATH.replace(/\//g, "|");
const DOC = `resourceRatings/${ID}`;

let env;
const as = (uid) => env.authenticatedContext(uid).firestore();
const fresh = (over = {}) => ({
  path: PATH,
  course: "se423",
  up: 1,
  down: 0,
  votes: { amal: 1 },
  updatedAt: FieldValue.serverTimestamp(),
  ...over,
});
const change = (over) => ({ updatedAt: FieldValue.serverTimestamp(), ...over });

before(async () => {
  env = await initializeTestEnvironment({
    projectId: "demo-shoug-resources",
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
    ctx
      .firestore()
      .doc(DOC)
      .set({
        path: PATH,
        course: "se423",
        up: 1,
        down: 1,
        votes: { sara: 1, noor: -1 },
        updatedAt: new Date(0),
      }),
  );
});

test("signed-out visitors can read tallies and query a course", async () => {
  const db = env.unauthenticatedContext().firestore();
  await assertSucceeds(db.doc(DOC).get());
  await assertSucceeds(
    db.collection("resourceRatings").where("course", "==", "se423").get(),
  );
});

test("signed-out visitors cannot vote", async () => {
  const db = env.unauthenticatedContext().firestore();
  await assertFails(db.doc(DOC).update(change({ up: 2, "votes.x": 1 })));
});

test("the first vote creates a valid tally", async () => {
  await env.clearFirestore();
  await assertSucceeds(as("amal").doc(DOC).set(fresh()));
});

test("a thumbs down can create a tally too", async () => {
  await env.clearFirestore();
  await assertSucceeds(
    as("amal")
      .doc(DOC)
      .set(fresh({ up: 0, down: 1, votes: { amal: -1 } })),
  );
});

test("create rejects stuffed or mismatched tallies", async () => {
  await env.clearFirestore();
  const db = as("amal").doc(DOC);
  await assertFails(db.set(fresh({ up: 50 })));
  await assertFails(db.set(fresh({ up: 0, down: 1 })));
  await assertFails(db.set(fresh({ votes: { amal: 5 } })));
  await assertFails(db.set(fresh({ votes: { sara: 1 } })));
  await assertFails(db.set(fresh({ votes: { amal: 1, sara: 1 }, up: 2 })));
  await assertFails(db.set(fresh({ extra: true })));
});

test("create rejects a doc id, path or course that disagree", async () => {
  await env.clearFirestore();
  await assertFails(as("amal").doc("resourceRatings/whatever").set(fresh()));
  await assertFails(
    as("amal")
      .doc(DOC)
      .set(fresh({ course: "cs101" })),
  );
  const outside = "/about/se423/x/";
  await assertFails(
    as("amal")
      .doc(`resourceRatings/${outside.replace(/\//g, "|")}`)
      .set(fresh({ path: outside })),
  );
});

test("a student can add, flip and remove their own vote", async () => {
  const db = as("amal").doc(DOC);
  await assertSucceeds(db.update(change({ up: 2, "votes.amal": 1 })));
  await assertSucceeds(db.update(change({ up: 1, down: 2, "votes.amal": -1 })));
  await assertSucceeds(
    db.update(change({ down: 1, "votes.amal": FieldValue.delete() })),
  );
});

test("a vote must move the tallies by exactly itself", async () => {
  const db = as("amal").doc(DOC);
  await assertFails(db.update(change({ up: 9, "votes.amal": 1 })));
  await assertFails(db.update(change({ "votes.amal": 1 })));
  await assertFails(db.update(change({ down: 0, "votes.amal": 1 })));
  await assertFails(db.update(change({ up: 3, "votes.amal": 2 })));
  await assertFails(db.update(change({ up: 50 })));
  // Already voted: re-sending the same vote can't count twice.
  await assertFails(
    as("sara")
      .doc(DOC)
      .update(change({ up: 2 })),
  );
});

test("a student cannot touch someone else's vote", async () => {
  const db = as("amal").doc(DOC);
  await assertFails(
    db.update(change({ down: 0, "votes.noor": FieldValue.delete() })),
  );
  await assertFails(db.update(change({ up: 2, down: 0, "votes.noor": 1 })));
  await assertFails(
    db.update(change({ up: 3, "votes.amal": 1, "votes.ghost": 1 })),
  );
});

test("identity fields are frozen and tallies can't be deleted", async () => {
  const db = as("sara").doc(DOC);
  await assertFails(db.update(change({ course: "cs101" })));
  await assertFails(db.update(change({ path: "/academics/a/cs101/b/" })));
  await assertFails(db.delete());
});
