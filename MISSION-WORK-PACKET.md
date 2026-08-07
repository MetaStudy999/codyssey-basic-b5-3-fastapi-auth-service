# B5-3 Mission Work Packet - Confirmed

## 1. Identity

- Mission: `B5-3` - 로그인이 되고 회원끼리 연결되는 웹 서비스 만들기
- Target: `MetaStudy999/codyssey-basic-b5-3-fastapi-auth-service`
- Control Tower: `MetaStudy999/codyssey-basic` **READ ONLY**
- Frozen baseline: `0d1581b3e82366988f57e1d76da311c028b8e15e`
- Active wave: `20260808-01`
- Mission repository baseline: `4d309ad7df51760c1219aa1fdb2c5dee96d5fe06`

## 2. Source Inventory

| Source | Path | State | Use |
|---|---|---|---|
| Mission PDF | `b5-3-mission.pdf` | VALID | 최고 우선 Mission Source |
| Mission Markdown | `b5-3-mission.md` | VALID | PDF 문장/구조를 Markdown으로 정리한 확인용 Source |
| Evaluation Markdown | `b5-3-evaluation.md` | VALID | 공식 평가문항 |
| Evaluation PDF | - | MISSING | 별도 PDF는 발견되지 않음 |
| Control Tower starter packet | `docs/00-governance/work-packets/b5-3.md` @ frozen baseline | VALID | 실행 프레임, requirement 자체는 Source 재검증 |

- Source Mode: `FULL SOURCE`
- Source Confidence: `HIGH`
- Source Gap: Evaluation PDF는 없지만 Evaluation Markdown이 실질 평가항목을 제공하므로 요구사항 확정에 차질 없음.

## 3. Dependency / Drift Check

Mission은 "이전 미션에서 구현한 웹 애플리케이션을 기반으로 확장"한다고 명시한다. 따라서 **교육적 연속성은 공식적으로 확인**된다. 다만 B5-3의 acceptance는 자체 Source에 인증/인가/모델/관계/상태변경/SSR/구조를 완결적으로 정의하고, B5-2 특정 commit/artifact를 제출하거나 동일 저장소 계보를 증명하라는 조건은 없다.

판정: `RECOMMENDED` code-reuse dependency, `NOT BUILD-BLOCKING`.

현재 B5-2 main에는 Source 문서만 있고 완성 구현이 없으므로 `WAITING-UPSTREAM`을 사용하지 않는다. 대신 B5-2에서 요구한 router/service/repository/ORM/SSR 계층 사고와 PRG 흐름을 그대로 유지한 superset 구조로 B5-3을 구현한다.

## 4. Mission Contract / Requirement Traceability

| ID | Confirmed requirement | Source | Planned evidence |
|---|---|---|---|
| REQ-01 | FastAPI `Depends` 기반 인증 | Mission §4.1 | `auth/dependencies.py`, auth tests |
| REQ-02 | session 또는 JWT 중 하나 + login/logout | Mission §4.1 | session auth, login tests |
| REQ-03 | 비로그인 보호 경로 차단 + 공개/보호 구분 | Mission §4.2 | redirect tests, README route table |
| REQ-04 | 인증 상태별 UI 변화 | Mission §4.3 | HTML assertion tests |
| REQ-05 | ORM model 3개 이상 | Mission §4.4 | User/Project/Task + mapper test |
| REQ-06 | 1:N/N:1 관계 2개 이상, back_populates 1개 이상 | Mission §4.4 | relationship introspection test |
| REQ-07 | 관계 데이터 화면 출력 | Mission §4.4 | Project detail owner + tasks test |
| REQ-08 | 부모 삭제 자식 처리 정책 + 이유 | Mission §4.4 | cascade code comment + delete test |
| REQ-09 | 상태 변경 business function | Mission §4.5 | Task pending/done service + test |
| REQ-10 | SQLAlchemy + relational DB persistence | Mission §4.6 | SQLite restart persistence test |
| REQ-11 | Jinja2 SSR 통합 사용자 흐름 | Mission §4.7 | TestClient end-to-end flow |
| REQ-12 | auth/router/service/repository/model/template 분리 | Mission §4.8 | repository tree + docs |
| REQ-13 | README 필수 항목 | Mission §4.9 | README |
| REQ-14 | 로그인/소유권을 서버에서 강제 | Workcell focus + Evaluation direct URL criterion | ownership/direct-url tests |

## 5. Evaluation Mapping

- 항목 1: 자동 integration test + README + SSR HTML assertions로 검증
- 항목 2: `docs/ARCHITECTURE.md`, model comments, service placement, cascade test로 검증
- 항목 3: `docs/LEARNING.md`와 코드 경로로 설명 가능 상태 확보
- 항목 4: architecture/learning 문서에 순환참조, 관리자 확장, REST 분리, 세션 확장성 질문 답변 포함

## 6. Scope / Non-scope

### In scope
- 세션 로그인/로그아웃
- 공개/보호 경로
- User/Project/Task
- 두 개의 1:N 관계
- owner 기반 authorization
- Task state transition
- SQLite/Jinja2 SSR
- tests/evidence/learning docs

### Non-scope / Backlog
- OAuth/social login
- 복잡한 RBAC
- 외부 클라우드 배포
- 별도 SPA 프론트엔드

## 7. Agent Routing

- Primary builder: ChatGPT workcell
- Automated harness: pytest + local HTTP runtime
- Review: requirement-to-code self-review + PR diff review
- 별도 Codex/Copilot 실행 인터페이스가 이 채팅에 노출되지 않으므로 독립 Agent 검토 결과를 허위로 기록하지 않는다.

## 8. Test / Runtime / Evidence Plan

1. `pytest -q`
2. `python -m compileall app tests`
3. Uvicorn 로컬 기동 + `/health` curl
4. 테스트 로그를 `evidence/test-results.md`에 실제 결과로 기록
5. PR diff에서 secret/password source 노출 점검

## 9. G1-G8 Checklist

- [x] G1 SOURCE - FULL SOURCE / HIGH
- [x] G2 BUILD - session auth + User/Project/Task + ownership/state service implemented
- [x] G3 TEST - compileall + pytest 10/10 PASS
- [x] G4 REVIEW - BLOCKER 0 / MAJOR 0 (self-review; no fake independent-agent claim)
- [x] G5 RUNTIME - local Uvicorn /health 200, protected URL 303 verified
- [x] G6 EVIDENCE - `evidence/test-results.md`
- [x] G7 LEARN - `docs/LEARNING.md`, `docs/ARCHITECTURE.md`
- [ ] G8 MERGE

## 10. STOP Rule

필수 Mission/Evaluation 요구 충족 + 필수 테스트 통과 + BLOCKER 0 + MAJOR 0 + Evidence 확보 시 종료한다. Bonus는 완료를 지연시키지 않는다.

## 11. Handoff Contract

최종 merge 뒤 `HANDOFF.md`와 `mission-result.yaml`에 Source Mode, tests, runtime, evidence, PR/SHA, Gate 상태, 남은 risk를 기록한다. Control Tower는 수정하지 않는다.
