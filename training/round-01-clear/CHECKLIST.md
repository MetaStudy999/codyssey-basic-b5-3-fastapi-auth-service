# B5-3 Round 01 — Mission Clear Checklist

현재 모드: **Phase A — REFERENCE BUILD**  
Runtime Mission 상태: **⬜ NOT STARTED**

> Reference 코드/문서가 있어도 실제 로그인·보호 URL·관계 데이터·상태 변경·DB/Evidence 전에는 CLEAR가 아닙니다.

## A. Source

- [x] `b5-3-mission.pdf` 확인
- [x] `b5-3-mission.md` 분석
- [x] `b5-3-evaluation.md` 분석
- [x] 필수/보너스/제약 분리
- [x] 세션 기반 인증 선택
- [x] Project/Task 서비스 주제 선택

## B. Reference Build

- [x] `REFERENCE-BUILD.md`
- [x] `reference/README.md`
- [x] `reference/requirements.txt`
- [x] `auth/`
- [x] `routers/`
- [x] `services/`
- [x] `repositories/`
- [x] `models/`
- [x] `templates/`
- [x] `environment/setup.sh`
- [x] `environment/verify.sh`
- [x] `environment/reset.sh`
- [x] `environment/inspect_db.py`
- [x] `docs/requirements-mapping.md`
- [x] `docs/evaluation-qa.md`
- [x] `evidence/README.md`
- [x] 상세 Beginner Guide

## C. 인증 / 인가 Reference

- [x] 로그인 GET/POST
- [x] 로그인 실패 메시지
- [x] 로그인 성공 session 저장
- [x] 로그아웃 session clear
- [x] `Depends(require_username)` 보호
- [x] 비로그인 보호 URL 303 `/login` 정책
- [x] 공개/보호 정책 README 표
- [x] 로그인 전/후 UI 분기
- [x] 테스트 계정 README 공개
- [x] `SESSION_SECRET` 환경 변수 사용

## D. 모델 / 관계 Reference

- [x] User 모델
- [x] Project 모델
- [x] Task 모델
- [x] User 1:N Project
- [x] Project 1:N Task
- [x] FK 2개 이상
- [x] `relationship + back_populates`
- [x] 관계 데이터 화면 출력
- [x] `cascade="all, delete-orphan"`
- [x] cascade 선택 이유 코드 주석
- [x] 관계 데이터 SQLite 저장

## E. 상태 변경 Reference

- [x] Task 진행중 상태
- [x] Task 완료 상태
- [x] 완료/미완료 토글
- [x] 상태 전환 Service 배치
- [x] 화면에 현재 상태/변경 버튼 표시

## F. 구조 / SSR

- [x] 인증/Router/Service/Repository/Model/Template 분리
- [x] Jinja2 SSR 주요 화면
- [x] SQLite + SQLAlchemy
- [x] `Depends(get_db)` DB Session
- [x] Project가 current User에 귀속되도록 조회 제한
- [x] Task 조회도 current User 소유 Project로 제한

## G. Reference 검증 설계

- [x] 파일 구조 검사
- [x] Python `compileall` 준비
- [x] 3모델 검사
- [x] FK 2개 검사
- [x] back_populates 검사
- [x] Depends 보호 검사
- [x] SessionMiddleware/SESSION_SECRET 검사
- [x] Service 상태 변경 검사
- [ ] 실제 `bash environment/verify.sh` 실행

## H. Runtime — Phase C

- [ ] Python 3.10+
- [ ] 가상환경/패키지 설치
- [ ] SESSION_SECRET 로컬 설정
- [ ] 서버 기동
- [ ] 로그인 전 UI
- [ ] 로그인 실패
- [ ] 정상 로그인
- [ ] 로그인 후 UI 변화
- [ ] 비로그인 보호 URL 직접 입력 차단
- [ ] Project 생성/조회
- [ ] 관계 데이터 화면 확인
- [ ] Task 생성
- [ ] 진행중 → 완료
- [ ] 완료 → 진행중
- [ ] 로그아웃
- [ ] 로그아웃 후 보호 URL 재차단
- [ ] database.db 생성
- [ ] User/Project/Task 관계 DB 직접 확인
- [ ] README 절차 재현

## I. Evaluation 설명

- [x] 인증/인가 Depends 흐름 답변 준비
- [x] 직접 URL 차단 위치 답변 준비
- [x] 레이어 분리 기준 답변 준비
- [x] 1:N 설계 이유 답변 준비
- [x] back_populates 설명 준비
- [x] cascade 정책 설명 준비
- [x] 상태 로직 Service 배치 이유 준비
- [x] 상태 변경 중요성 설명 준비
- [x] 양방향 관계 순환 참조 주의 설명 준비
- [x] 관리자 역할 확장 설명 준비
- [x] REST frontend 분리 시 인증 변화 설명 준비
- [x] 세션 확장성 장단점 설명 준비
- [ ] 사용자가 Runtime 근거로 자기 말로 설명

## J. Evidence / CLEAR

- [x] Evidence 계획
- [ ] 인증 전/후 Evidence
- [ ] 보호 URL Evidence
- [ ] 관계 데이터 Evidence
- [ ] 상태 전/후 Evidence
- [ ] DB Evidence
- [ ] 구조 Evidence
- [ ] Secret 노출 없음 최종 확인
- [ ] BLOCKER 0 / MAJOR 0 최종 감사
- [ ] **✅ B5-3 CLEAR**
