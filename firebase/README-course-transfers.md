# Ethics bank-transfer checkout

Routes:

- `/checkout/ethics/`: existing Firebase login, verified email, SAR 325 bank instructions, required receipt photo, purchase status.
- `/admin/transfers/`: administrator-only receipt review beside each buyer's authenticated email; approve or reject with a correction note.

Uses the site's existing Firebase Auth and Firestore project. No payment gateway,
email notification service, or Cloud Storage subscription is added. Firestore
usage still counts against the project's existing quota/billing plan. Receipts
are re-encoded to JPEG and capped at 700,000 characters inside private documents
to avoid needing a separate upload bucket. The list loads at most ten receipts
at once. There is no promise of unlimited free hosting.

## Required setup before accepting payments

1. In Firebase Console, inspect the **current** Firestore rules. Merge the
   functions and matches in `course-transfers.rules` into the existing
   `/databases/{database}/documents` match. Do not replace unrelated rules.
   Remove/narrow any broad wildcard grants that would also authorize these
   collections: Firestore matching allow rules are ORed, so a catch-all grant
   defeats the restrictions. Test the merged production rules too.
2. Identify the owner's verified Firebase Authentication account and copy its
   UID (not its email) from Authentication > Users. Do not infer the UID from the
   publicly listed contact email. The owner must sign in with that account.
3. In Firestore Console create `courseCommerce/ethics` with these fields:

   | Field       | Type    | Value                                        |
   | ----------- | ------- | -------------------------------------------- |
   | enabled     | boolean | **false** until all launch checks pass       |
   | adminUid    | string  | Verified owner account's Firebase UID        |
   | bankName    | string  | Actual bank name supplied by owner           |
   | beneficiary | string  | Actual bank account beneficiary              |
   | iban        | string  | Actual Saudi IBAN, uppercase, without spaces |

   Optional string fields `stcPhone` and `barqPhone` show mobile-transfer alternatives. Use international format `+9665XXXXXXXX`.

   These receiving details are shown to signed-in buyers. Client applications,
   including the admin page, cannot change the configuration. No fake bank
   details are included in production files.

4. Deploy the HTML/JS/CSS through the existing website release workflow.
5. The course access Worker now protects paid content on the custom domain.
   See `workers/course-access/README.md` for private-source updates and the
   remaining public GitHub origin/history limitations. Keep the bank-transfer
   feature closed until the production rules and owner account are configured.
6. Validate with a buyer account and a separate owner account: login required,
   upload and preview readable, pending status, owner sees email + receipt,
   approval/rejection, corrected resubmission, and access enforced at the asset
   origin. Set `enabled` true only when bank details and protected delivery work.

## Review behavior

One order per Firebase UID for this course prevents accidental duplicate orders.
The price is stored in halalas (`32500`) and enforced by database rules. Buyer
email is matched to the verified authentication token. Buyers cannot approve,
delete, overwrite pending/approved orders, or read another buyer's proof.
Admins can review pending orders only; a rejected buyer may resubmit. Approval
is a database status, not evidence of a bank reconciliation API. The owner must
check the actual bank credit. Proof is shown with email in the private dashboard;
no receipt emails are sent. Only a trusted backend/console can correct an
approved record or delete old receipts according to the owner's retention policy.

## Security tests

Requires Node 20+ and Java. Install test dependencies in a temporary directory:

```sh
npm install --prefix /tmp/shoug-transfer-tests firebase@10.12.0 @firebase/rules-unit-testing@3.0.4 firebase-tools@14.15.2 jsdom@24
NODE_PATH=/tmp/shoug-transfer-tests/node_modules node --test tests/course-transfers/ui.test.cjs
NODE_PATH=/tmp/shoug-transfer-tests/node_modules node --test tests/course-transfers/verification.test.cjs
NODE_PATH=/tmp/shoug-transfer-tests/node_modules /tmp/shoug-transfer-tests/node_modules/.bin/firebase emulators:exec --project demo-shoug-transfers --config firebase/course-transfers.emulator.json --only firestore 'node --test tests/course-transfers/rules.test.cjs'
```

The demo project and emulator never connect to production data. This standalone
ruleset deliberately grants no access to the site's unrelated collections.

Registration records require `fullName` (2–120 characters) and `phone` (international +country-code format), plus the verified account email. Publish the updated rules before enabling enrollment. The reviewer sees these fields beside the receipt.

## Activation — October 1, 2026

Merged and published the course rules through Firebase Console while preserving the existing profiles, comments, reactions, and progress rules. Created `courseCommerce/ethics` with enrollment enabled and the owner UID verified from Authentication for shoug.alomran@hotmail.com. Bank details and STC/Barq alternatives are configured. Review submissions at `/admin/transfers/`; approval requires confirming the payment arrived. No email attachment delivery is configured: receipts are reviewed privately on the website.
