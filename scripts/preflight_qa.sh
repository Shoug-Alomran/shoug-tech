#!/usr/bin/env bash
# Check the committed docs/ site before a release: rebuild the page
# inventories, optimize the HTML, then check routes, links and SEO metadata.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/5] Regenerating page inventories..."
node scripts/build-course-manifest.js
node scripts/build-search-index.js

echo "[2/5] Optimizing the docs/ HTML..."
python3 scripts/optimize_site_html.py

echo "[3/5] Verifying generated course routes..."
python3 scripts/verify_site_routes.py

echo "[4/5] Checking internal links and assets..."
python3 scripts/check_site_links.py

echo "[5/5] Checking SEO metadata..."
python3 scripts/check_seo_metadata.py

echo "Preflight QA passed."
