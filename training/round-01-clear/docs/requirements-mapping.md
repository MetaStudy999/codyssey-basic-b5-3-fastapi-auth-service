# B5-3 Requirement → Implementation → Verification → Evidence

Source of Truth: `b5-3-mission.pdf` → `b5-3-mission.md` → `b5-3-evaluation.md`.

| ID | 공식 요구사항 | Reference 구현 | 검증 | Phase C Evidence |
|---|---|---|---|---|
| R01 | 로그인/로그아웃 | `routers/auth.py`, session | 성공/실패/로그아웃 브라우저 흐름 | 화면/응답 기록 |
| R02 | Depends 기반 인증 | `auth/dependencies.py: require_username` | 보호 URL 직접 접근 | 로그인 Redirect 기록 |
| R03 | 공개/보호 경로 구분 | `reference/README.md` 정책 표 + `/app/**` 보호 | 각 경로 직접 접근 | 경로별 결과 |
| R04 | 로그인 상태별 UI 변화 | `templates/base.html` | 전/후 메뉴 비교 | 전/후 화면 |
| R05 | 최소 3 ORM 모델 | User, Project, Task | DB/table/code 확인 | DB/구조 출력 |
| R06 | 관계 2개 이상 | User 1:N Project, Project 1:N Task | FK/relationship 확인 | 관계 화면/DB |
| R07 | 양방향 back_populates | `models/domain.py` | 코드 검사 | 코드 근거 |
| R08 | 관계 데이터 화면 출력 | project owner + task 목록 | 프로젝트 화면 | 화면 캡처 |
| R09 | 부모 삭제 정책 | 두 관계 `cascade="all, delete-orphan"` + 주석 | 코드 설명 | 평가 설명 |
| R10 | 상태 변경 기능 | `ProjectService.toggle_task()` | 진행중↔완료 | 전/후 화면 |
| R11 | 상태 로직 Service 위치 | `services/project_service.py` | 코드 검사 | 설명 |
| R12 | ORM + 관계형 DB 저장 | SQLite/SQLAlchemy | `database.db`, `inspect_db.py` | DB 출력 |
| R13 | 모든 주요 화면 Jinja2 SSR | templates + TemplateResponse | 브라우저 | 주요 화면 |
| R14 | 통합 흐름 | login→project→task→toggle | E2E 수동 확인 | 흐름 기록 |
| R15 | 역할 분리 | auth/routers/services/repositories/models/templates | tree/code | 구조 출력 |
| R16 | README 필수 정보 | 실행/버전/계정/경로/인증 이유 | README 검토 | 재현 결과 |
| R17 | Python 3.10+ | Environment Golden Path | `python --version` | 버전 출력 |
| R18 | 허용 라이브러리 범위 | 핵심 5종 + `itsdangerous` | requirements 확인 | 파일 |

## 범위 분리

회원가입/비밀번호 해싱, OAuth2 소셜 로그인, 검색, 전역 예외처리, 외부 배포는 공식 보너스이므로 필수 CLEAR Gate로 승격하지 않습니다.

## 상태 원칙

Reference 코드 존재는 Runtime PASS가 아닙니다. 로그인 차단, 세션 유지, 관계 데이터, 상태 변경, DB 저장은 Phase C 실제 실행으로만 확정합니다.
