# B5-3 Evidence - Test & Runtime Results

실행일: 2026-08-08 (KST)

## 1. Syntax / import validation

Command:

```bash
python -m compileall -q app tests
```

Result: **PASS** - 오류 출력 없음.

## 2. Automated tests

Command:

```bash
pytest -q
```

Actual result:

```text
..........                                                               [100%]
10 passed in 1.04s
```

Coverage by behavior:

- login success/failure/logout
- anonymous direct protected URL redirect
- auth-aware SSR UI
- 3 models and two bidirectional relationships
- relation data rendered in project detail
- project/task ownership enforcement across `demo` and `alice`
- `pending -> done -> pending` state transition
- invalid duplicate transition rejected by service
- project deletion cascades child tasks
- SQLite persistence across app recreation

## 3. Local Uvicorn runtime

Command shape:

```bash
SESSION_SECRET='<ephemeral runtime value>' \
DATABASE_URL='sqlite:////tmp/b5_3_runtime.db' \
uvicorn app.main:app --host 127.0.0.1 --port 8013
```

The runtime value itself was not committed or recorded.

Actual checks:

```text
GET /health          -> 200 {"status":"ok"}
GET /app/projects    -> 303 Location: /login?next=/app/projects
GET /                -> 200, "로그인하고 시작하기" present
```

Uvicorn reached normal startup and normal shutdown.

## 4. Security/secret review

- `.env`, DB files, caches are ignored.
- No private API key/private key material is present.
- `SESSION_SECRET` is read from environment or generated ephemerally; no real secret is committed.
- README contains only the **public mission test accounts** explicitly required by the Mission.
- Demo seed source stores PBKDF2 salt/hash, not plaintext password values.

## 5. Review severity

- BLOCKER: 0
- MAJOR: 0

Review method: requirement-to-code self review + automated test harness + runtime checks. A separate Codex/Copilot execution interface was not available in this workcell, so no independent-agent PASS is claimed.

## 6. Manual visual acceptance

The server-side HTML and authentication-state text are asserted by automated tests. A human browser screenshot is optional in the Mission and was not fabricated. Status: **NOT REQUIRED / optional evidence**.
