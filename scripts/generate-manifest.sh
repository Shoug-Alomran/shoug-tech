#!/usr/bin/env bash
# Run this whenever you add, remove, or rename academic pages.
# Usage: bash scripts/generate-manifest.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
node "$ROOT/scripts/build-course-manifest.js"
