# Ethics course access

The Cloudflare Worker runs before assets on all paid course routes. It validates
the Firebase ID token with Firebase, then reads the buyer's Firestore order using
that token. Only an approved SAR 325 ethics purchase or the configured admin UID
can retrieve course HTML, PDFs, images, transcripts, question data or videos.
Signed-in users with pending/rejected orders do not receive paid content.

Private HTML is bundled in the Worker assets binding with `run_worker_first:
true`; workers.dev and preview URLs are disabled. Videos are in the private
`shoug-ethics-private` R2 bucket. Its 36 original `videos/ethics/` public objects
were copied, checked for size/source ETag, and retired on October 1, 2026. Other
objects in the `videos` bucket were unchanged. Do not re-enable public access on
the new bucket. Upload scripts now target the private bucket; existing storage
credentials may need scope for that bucket before future uploads.

## Local source and updates

The original paid source is preserved at `.private-courses/ethics/` (ignored by
Git). Public `docs/academics/other-courses/ethcs303/` files are access gates; they
are **not** the lesson source. The archived source is also in deployed Worker
assets. Back up the private source separately before cleaning ignored files.

Build and deploy after editing private source or checkout:

```sh
python3 scripts/secure_ethics_content.py --build-worker --seal --check
node --test workers/course-access/src/index.test.js
wrangler whoami
wrangler deploy --config workers/course-access/wrangler.jsonc
```

The Pages workflow seals paid content after generators run. It must not publish
new private lessons. If using an old generator that writes to `docs`, archive its
intentional updates with `--archive` before sealing again. **Never run --archive
against arbitrary regenerated content without reviewing it.**

The public GitHub repository and its historical commits remain public by owner
request. The existing GitHub Pages origin also needs the pending repository
changes published. The live custom-domain Worker cannot revoke content already
copied or obtained directly from public Git history. No repository visibility or
history changes have been made.

## Checkout and verification

Checkout and its assets are served by this Worker too, so the updated UI is live
without including unrelated working-tree changes in a GitHub push. Unverified
buyers automatically receive one verification email; the page reloads their
Firebase account on a timer and when they return to the tab, refreshes the token,
and proceeds without an “I've verified” button. Automatic sends are deduplicated
for 10 minutes; a recovery resend is available after 60 seconds. An already-used
link is not reused: the watcher recognizes an account that is already verified.
Genuinely expired links need a fresh email. Email ownership must still be verified
by opening the email link; it is never inferred from a URL flag.

See `firebase/README-course-transfers.md` for the still-required bank/admin
configuration and production Firestore rules. No fake bank details or admin
identity were filled in. Until configured, checkout remains closed. Approval
must be based on an actual bank credit, not just an uploaded screenshot.

The gate uses an HttpOnly Secure same-site cookie. Every protected request
rechecks approval; protected responses are `private, no-store`. The site's
service worker excludes course/checkout/admin routes and drops older caches.
Video byte ranges are authorized before R2 access. The checkout and private
lessons do not include session replay.

## Free samples

`/course-access/samples/` serves the selected opening-topic mindmap and slide breakdown, and an explicit `intro-video.mp4` alias for Divine Command Theory. Other lesson video paths remain authenticated. The public samples are in `docs/course-access/samples/` and copied by the private-assets build.
