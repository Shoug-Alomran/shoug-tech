# Search indexing repairs

This Worker supplements the existing GitHub Pages origins. It does not host the
site. Deployment is **pending explicit approval**: automatic approval review
blocked the first deployment attempt; no live changes were made.

## Behavior

- 296 verified legacy academic paths redirect to existing files/pages. This
  includes the old mixed-case SE201 Software Processes URL and uniquely matched
  flat PDF paths that moved into topic folders.
- 499 PDF response URLs receive an absolute `Link: ...; rel="canonical"` header.
  A PDF points to its containing page only when that page actually embeds it;
  other PDFs use their own URL. PDF bytes, downloads and range responses survive.
- Six obsolete Operating Systems `.md` URLs redirect to published HTML pages.
  Narrow robots Allow rules permit Google to discover those redirects.
- The old Database Phase 3 PDF redirects to the published Phase 3 report.
  Robots also permits crawling the removed `Phase-0/Project plan.html` so Google
  can observe its 404. There is no verified replacement for that retired page;
  redirecting it to unrelated content would be misleading.
- Lilly Kitchen `/en` and `/ar` receive self-canonicals and reciprocal language
  alternate tags in server HTML. Login pages are unchanged.

Route scope is limited to three public static sections on the primary domain,
the one old SE201 URL, and the relevant subdomain prefixes. There are no whole
domain `/*` routes. Requests outside the explicit rules pass through unchanged.
The existing Cloudflare zone had no Worker routes when inspected on 2026-09-15.

## Validation and release

Use Node 22 or later. From this directory:

```sh
npm install
npm run build
npm test
npx wrangler deploy --dry-run
npx wrangler whoami
# After explicit production approval:
npm run deploy
```

The primary site's CI rebuilds the manifest and tests the rules, but does not
deploy this Worker. Regenerate and redeploy it when PDF paths change. GitHub
Pages does not support `_headers`; putting such a file there would not fix PDFs.

After deploying, verify redirects with `curl -IL --max-redirs 8`, PDF canonical
headers with `curl -I`, Lilly Kitchen tags with a GET, and both robots files.
Rollback by removing only this Worker's routes in Cloudflare, restoring direct
origin handling; never delete unrelated Workers or DNS records.

## Search Console follow-up

Live checks on 2026-09-15 found all four reported redirect-error examples healthy:
ISC113 lecture-11 redirects once to a 200 page, and all three Blueprint paths
return 200 without HTTP redirects. The reported SE201 5xx is now a 404; its repair
is included here. Existing sitemap and metadata checks pass.

The 178 alternate pages include embedded HTML documents whose canonicals point
to their study wrappers. Preserve these valid signals. HTTP/www redirects,
login exclusions and internal-search exclusions are also expected.

After deployment, request validation for repaired duplicate, redirect-error,
server-error and public robots-blocked groups in Search Console. Do not request
indexing of login/search pages or replace correct alternate canonicals. Counts
will not clear until Google recrawls; indexing is Google's decision. Screenshots
only show the first page of examples, so unseen URLs need the full report export
or Search Console access to confirm every case.

References: [Google canonical headers](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls),
[Google redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects).
