#!/usr/bin/env bash
set -u

ROUND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF_DIR="$ROUND_DIR/reference"
APP_DIR="$REF_DIR/app"
PASS=0
FAIL=0

pass(){ printf '[PASS] %s\n' "$1"; PASS=$((PASS+1)); }
fail(){ printf '[FAIL] %s\n' "$1"; FAIL=$((FAIL+1)); }

for path in \
  "$REF_DIR/requirements.txt" \
  "$APP_DIR/main.py" \
  "$APP_DIR/auth/dependencies.py" \
  "$APP_DIR/models/domain.py" \
  "$APP_DIR/repositories/domain_repository.py" \
  "$APP_DIR/services/project_service.py" \
  "$APP_DIR/routers/auth.py" \
  "$APP_DIR/routers/projects.py" \
  "$APP_DIR/templates/login.html" \
  "$APP_DIR/templates/projects/list.html" \
  "$APP_DIR/templates/projects/detail.html"
do
  [[ -f "$path" ]] && pass "file exists: ${path#$ROUND_DIR/}" || fail "missing: ${path#$ROUND_DIR/}"
done

if command -v python3 >/dev/null 2>&1 && python3 -m compileall -q "$APP_DIR"; then
  pass "Python syntax compileall"
else
  fail "Python syntax compileall"
fi

MODEL_FILE="$APP_DIR/models/domain.py"
if grep -q 'class User' "$MODEL_FILE" && grep -q 'class Project' "$MODEL_FILE" && grep -q 'class Task' "$MODEL_FILE"; then
  pass "three ORM models present"
else
  fail "three ORM models present"
fi

if [[ "$(grep -c 'back_populates=' "$MODEL_FILE")" -ge 4 ]]; then
  pass "bidirectional back_populates relationships present"
else
  fail "bidirectional back_populates relationships present"
fi

if [[ "$(grep -c 'ForeignKey' "$MODEL_FILE")" -ge 2 ]]; then
  pass "two relationship foreign keys present"
else
  fail "two relationship foreign keys present"
fi

if grep -q 'Depends(require_username)' "$APP_DIR/routers/projects.py"; then
  pass "protected routes use Depends auth"
else
  fail "protected routes use Depends auth"
fi

if grep -q 'SessionMiddleware' "$APP_DIR/main.py" && grep -q 'SESSION_SECRET' "$APP_DIR/main.py"; then
  pass "session middleware uses environment secret"
else
  fail "session middleware uses environment secret"
fi

if grep -q 'task.is_done = not task.is_done' "$APP_DIR/services/project_service.py"; then
  pass "state-change rule located in service"
else
  fail "state-change rule located in service"
fi

printf 'Result: %d PASS / %d FAIL\n' "$PASS" "$FAIL"
[[ "$FAIL" -eq 0 ]]
