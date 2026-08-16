# B5-3 Round 01 — CLEAR

구분: **선택 미션 (OPTIONAL)**  
현재 모드: **Phase A — REFERENCE BUILD**  
Runtime Mission 상태: **⬜ NOT STARTED**

## 선행 학습

- **필수 선행 미션:** 없음
- **권장 선행 미션:** B5-2, B5-1
- **있으면 좋은 선행 지식:** Session, Authentication/Authorization, 관계형 DB, CRUD

B5-2의 CRUD 구조와 B5-1의 관계형 DB 개념을 먼저 익히면 인증·관계·세션을 추가하는 흐름이 자연스럽습니다. 다만 CRUD와 관계형 DB 기초가 이미 있다면 두 미션을 CLEAR하지 않고도 B5-3를 시작할 수 있습니다.

## 현재 판정

B5-3의 세션 인증 + User/Project/Task 관계 + Task 상태 변경 **Reference 핵심 기준본을 준비했습니다.** 실제 Runtime/Evidence 전이므로 아직 `✅ CLEAR`가 아닙니다.

## 핵심 문서

- `REFERENCE-BUILD.md`
- `REFERENCE-STATUS.md`
- `BEGINNER-GUIDE.md`
- `CHECKLIST.md`
- `reference/README.md`
- `docs/requirements-mapping.md`
- `docs/evaluation-qa.md`
- `evidence/README.md`

## 기준 구현 핵심

- 세션 기반 로그인/로그아웃
- `Depends(require_username)` 보호
- 공개/보호 URL 정책
- 로그인 전/후 UI
- User 1:N Project 1:N Task
- `back_populates`
- `cascade="all, delete-orphan"`
- Task 진행중↔완료 상태 변경
- Jinja2 SSR + SQLite/SQLAlchemy

Reference 코드가 존재한다는 이유만으로 Runtime PASS를 표시하지 않습니다.
