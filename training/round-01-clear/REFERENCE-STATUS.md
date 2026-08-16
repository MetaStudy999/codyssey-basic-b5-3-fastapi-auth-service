# B5-3 R01 — Reference Status

## Phase A 준비 결과

- [x] Source/Evaluation 분석
- [x] 세션 기반 인증 선택
- [x] `SessionMiddleware` + env `SESSION_SECRET`
- [x] `Depends(require_username)` 보호 경로
- [x] 로그인 성공/실패/로그아웃
- [x] 로그인 전/후 UI 변화
- [x] 테스트 계정/공개·보호 정책 README
- [x] User/Project/Task 3 ORM 모델
- [x] 1:N 관계 2개
- [x] bidirectional `back_populates`
- [x] cascade 정책 + 코드 주석
- [x] 관계 데이터 SSR 출력
- [x] Task 진행중/완료 상태 변경
- [x] 상태 변경 로직 Service 배치
- [x] SQLite/SQLAlchemy 저장
- [x] 구조 분리 auth/router/service/repository/model/template
- [x] Reference verify/setup/reset/DB inspect
- [x] Requirements Mapping
- [x] Evaluation Q&A
- [x] Evidence Guide
- [x] Beginner Guide
- [x] Checklist
- [x] SQLite runtime Git ignore

## Phase C에서만 완료

- [ ] 실제 Python/가상환경/패키지
- [ ] 실제 `verify.sh`
- [ ] 실제 session secret local input
- [ ] 실제 server/browser
- [ ] 로그인 실패/성공/로그아웃
- [ ] 보호 URL 직접 접근 차단
- [ ] 로그인 전/후 UI
- [ ] Project/Task 관계 화면
- [ ] Task 상태 변경 전/후
- [ ] SQLite 관계 데이터
- [ ] README 재현
- [ ] Runtime Evidence
- [ ] 사용자 자기 말 평가 설명
- [ ] BLOCKER/MAJOR 최종 Gate
- [ ] `✅ B5-3 CLEAR`

## 판정

**Reference 핵심 기준본 준비 완료 / Runtime 미시작 / CLEAR 아님**
