# AGENTS.md - B5-3 Review Contract

## Source of Truth
1. `b5-3-mission.pdf`
2. `b5-3-mission.md`
3. `b5-3-evaluation.md`
4. `MISSION-WORK-PACKET.md`

## Review scope
Report only BLOCKER or MAJOR issues that can prevent mission acceptance:
- missing confirmed Mission/Evaluation requirement
- authentication not enforced with FastAPI Depends
- unauthenticated direct protected URL bypass
- cross-user ownership bypass
- model/relationship/count/back_populates requirement failure
- business state transition missing/broken
- test failure or false PASS
- secret/credential exposure beyond documented public test accounts

## Preserve
- beginner-readable router/service/repository/model split
- Jinja2 SSR and session-based authentication choice
- simple User -> Project -> Task domain
- learning documents matching the code

## Do not do
- replace the architecture
- add OAuth/social login/RBAC/cloud deployment
- large refactor for style only
- mark unexecuted checks PASS

## Test commands
```bash
python -m compileall app tests
pytest -q
```

## Stop condition
BLOCKER=0 and MAJOR=0 with the required tests passing.
