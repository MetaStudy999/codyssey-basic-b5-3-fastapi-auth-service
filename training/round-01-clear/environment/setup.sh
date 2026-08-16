#!/usr/bin/env bash
set -euo pipefail

ROUND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF_DIR="$ROUND_DIR/reference"
cd "$REF_DIR"

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

printf '[PASS] B5-3 virtual environment prepared.\n'
printf '[INFO] Before server start, export SESSION_SECRET locally. Do not commit or share the value.\n'
