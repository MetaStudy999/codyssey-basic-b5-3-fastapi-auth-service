# Codyssey Basic B5-3

## 구분
- 선택 미션 (OPTIONAL)
- 현재 훈련 체계: Round 01 — CLEAR
- 현재 작업 모드: Phase A — REFERENCE BUILD

## 시작 위치
`training/round-01-clear/BEGINNER-GUIDE.md`부터 진행합니다.

## 공식 원본
- `b5-3-mission.pdf`
- `b5-3-mission.md`
- `b5-3-evaluation.md`

공식 원본은 수정하지 않습니다.

## Round 01 Reference Build

`training/round-01-clear/reference/`에 Project Task 서비스 기준본을 준비했습니다.

핵심:
- 세션 기반 로그인/로그아웃
- `Depends` 기반 보호 경로
- 로그인 전/후 UI
- User / Project / Task 3모델
- 1:N 관계 2개 + `back_populates`
- cascade 정책
- Task 진행중↔완료 상태 변경
- Jinja2 SSR + SQLite/SQLAlchemy
- setup/verify/reset/DB inspection
- Requirements Mapping / Evaluation Q&A / Evidence Guide

테스트 계정은 공식 요구에 따라 Reference README에 공개한 로컬 학습용 계정입니다. 실제 `SESSION_SECRET` 값은 저장소에 저장하지 않습니다.

## 상태

**Reference 핵심 기준본 준비 완료 / Runtime 미시작 / `✅ CLEAR` 아님**
