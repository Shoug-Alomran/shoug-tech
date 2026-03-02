#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/3] Checking EN/AR markdown parity (strict)..."
python3 scripts/check_i18n_parity.py --autofix-missing-ar --strict

echo "[2/3] Building MkDocs site..."
mkdocs build --clean

echo "[3/3] Verifying favicon exists..."
test -f docs/favicon.ico

echo "Preflight QA passed."
