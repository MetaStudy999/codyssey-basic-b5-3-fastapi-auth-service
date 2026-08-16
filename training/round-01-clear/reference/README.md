# B5-3 Reference — Project Task Auth Service

공식 B5-3 Mission/Evaluation을 위한 **세션 기반 Reference 기준본**입니다. 실제 Runtime PASS/Evidence는 Phase C에서 사용자 환경에서 검증합니다.

## 서비스 주제

`User → Project → Task` 관계를 가진 할 일 관리 서비스입니다.

- User 1:N Project
- Project 1:N Task
- `relationship + back_populates` 양방향 관계 사용
- Task 상태: `진행중 ↔ 완료`

## 인증 방식

**방식 A — 세션 기반**을 선택했습니다.

이유:
- Jinja2 SSR 브라우저 흐름과 직접 연결하기 쉽습니다.
- 로그인 성공 후 세션 쿠키를 통해 이후 보호 요청을 식별할 수 있습니다.
- `Depends(require_username)`으로 보호 경로의 인증 Gate를 코드에서 명확히 보여줄 수 있습니다.

`SessionMiddleware`의 서명 키는 저장소에 넣지 않고 환경 변수 `SESSION_SECRET`으로 받습니다.

## 테스트 계정

공식 미션이 README에 테스트 계정 ID/PW 명시를 요구하므로 아래 **로컬 학습용 계정**을 공개합니다.

| ID | PW |
|---|---|
| `demo` | `demo1234` |

실서비스 계정이 아니며 B5-3 Reference Runtime 전용입니다.

## 공개 / 보호 경로 정책

| 경로 | 메서드 | 정책 | 목적 |
|---|---|---|---|
| `/` | GET | 공개 | 홈 |
| `/login` | GET/POST | 공개 | 로그인 |
| `/logout` | POST | 로그인 상태에서 사용 | 로그아웃 |
| `/app/projects` | GET | 보호 | 내 프로젝트 목록 |
| `/app/projects/new` | GET | 보호 | 프로젝트 생성 폼 |
| `/app/projects` | POST | 보호 | 프로젝트 생성 |
| `/app/projects/{id}` | GET | 보호 | 관계 데이터/Task 목록 |
| `/app/projects/{id}/tasks` | POST | 보호 | Task 생성 |
| `/app/tasks/{id}/toggle` | POST | 보호 | Task 상태 변경 |

보호 경로는 `Depends(require_username)`을 통과하지 못하면 `/login`으로 이동하도록 303 응답을 냅니다.

## 구조

```text
reference/app/
├── main.py
├── database.py
├── auth/
│   └── dependencies.py
├── routers/
│   ├── home.py
│   ├── auth.py
│   └── projects.py
├── services/
│   └── project_service.py
├── repositories/
│   └── domain_repository.py
├── models/
│   └── domain.py
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── not_found.html
    └── projects/
        ├── list.html
        ├── new.html
        └── detail.html
```

## 실행 — Phase C

```bash
cd training/round-01-clear/reference
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export SESSION_SECRET='로컬에서만_사용할_충분히_긴_임의값'
uvicorn app.main:app --reload
```

`SESSION_SECRET` 실제 값은 채팅/Git/Evidence에 기록하지 않습니다.

브라우저: `http://localhost:8000`

## 주요 확인 흐름

```text
비로그인 홈
→ 보호 URL 직접 접근
→ 로그인 화면 이동
→ demo 로그인
→ UI 변화
→ Project 생성
→ Task 생성
→ 진행중 확인
→ 완료 토글
→ 완료 확인
→ 로그아웃
→ 보호 URL 재차단
```

## 부모 삭제 정책

`User.projects`, `Project.tasks`에 `cascade="all, delete-orphan"`을 사용합니다. 부모가 제거될 때 소속 자식이 orphan으로 남지 않도록 하는 정책이며 코드 주석에 이유를 남겼습니다.

## 범위 제한

- 회원가입/비밀번호 해싱은 보너스이므로 구현하지 않습니다.
- OAuth2 소셜 로그인은 보너스이므로 구현하지 않습니다.
- 복잡한 역할 기반 권한 체계는 구현하지 않습니다.
- 외부 배포는 보너스이므로 Phase A Reference 필수 범위에 넣지 않습니다.
