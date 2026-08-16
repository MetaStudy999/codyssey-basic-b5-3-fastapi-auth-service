#!/usr/bin/env bash
set -euo pipefail

ROUND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF_DIR="$ROUND_DIR/reference"

rm -rf "$REF_DIR/.venv"
rm -f "$REF_DIR/database.db" "$REF_DIR/database.db-shm" "$REF_DIR/database.db-wal"
find "$REF_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +

printf '[PASS] Removed only B5-3 R01 generated .venv/database/cache artifacts.\n'
