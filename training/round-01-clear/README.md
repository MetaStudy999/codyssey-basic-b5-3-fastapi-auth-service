# B5-3 Round 01 — CLEAR

구분: **선택 미션 (OPTIONAL)**  
현재 모드: **Phase A — REFERENCE BUILD**  
Runtime Mission 상태: **⬜ NOT STARTED**

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
