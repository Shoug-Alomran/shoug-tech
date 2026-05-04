#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/4] Checking EN/AR markdown parity (strict)..."
python3 scripts/check_i18n_parity.py --autofix-missing-ar --strict

echo "[2/4] Building MkDocs site..."
mkdocs build --clean

echo "[3/4] Verifying generated course routes..."
python3 scripts/verify_site_routes.py

echo "[4/4] Verifying configured theme assets exist..."
python3 - <<'PY'
from pathlib import Path
import re
import sys

root = Path(".")
config_text = (root / "mkdocs.yml").read_text(encoding="utf-8")

required = []
for key in ("favicon", "logo"):
    match = re.search(rf"(?m)^  {re.escape(key)}:\s+(.+?)\s*$", config_text)
    if match:
        value = match.group(1).strip().strip("'\"")
        required.append((key, root / "docs" / value))

missing = [(key, path) for key, path in required if not path.exists()]
if missing:
    for key, path in missing:
        print(f"[error] theme {key} asset not found: {path}")
    sys.exit(1)

for key, path in required:
    print(f"[ok] theme {key}: {path}")
PY

echo "Preflight QA passed."
