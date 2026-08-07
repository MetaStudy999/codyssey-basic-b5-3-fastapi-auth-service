# Codyssey Basic B5-3 - FastAPI Auth Service

`Depends` 기반 인증/인가, SQLAlchemy 연관관계, 상태 전이 비즈니스 로직을 Jinja2 SSR로 통합한 **Project Flow** 학습 서비스입니다.

## 핵심 기능

- 세션 기반 로그인/로그아웃
- `Depends(require_user)`를 통한 서버 측 보호 경로 강제
- 로그인 전/후 네비게이션 UI 변화
- SQLAlchemy 모델 3개: `User`, `Project`, `Task`
- 관계 2개: `User 1:N Project`, `Project 1:N Task`
- 양방향 `relationship + back_populates`
- 사용자 소유권 기반 프로젝트/할 일 접근 제어
- 상태 전이: `Task pending -> done -> pending`
- 프로젝트 삭제 시 소속 Task `delete-orphan` cascade
- SQLite 영구 저장 + Jinja2 SSR

## 인증 방식 선택

**세션 기반 인증**을 선택했습니다. 이 미션은 Jinja2 서버 사이드 렌더링(SSR)이 중심이므로 브라우저 쿠키와 서버 요청 흐름을 직접 연결하기 쉽고, JWT를 추가하는 것보다 요구 범위가 작고 설명 가능성이 높습니다. `SessionMiddleware`는 서명된 세션 쿠키를 사용하고, 실제 보호 여부는 UI가 아니라 `Depends(require_user)`에서 서버 측으로 검사합니다.

`SESSION_SECRET`은 저장소에 넣지 않습니다. 미설정 시 학습용 단일 프로세스에서만 쓸 수 있는 임시 키가 프로세스 시작 시 생성됩니다. 재시작 후에도 로그인 세션을 유지해야 하거나 운영 배포를 한다면 반드시 환경변수로 고정하세요.

## 테스트 계정

| ID | PW | 표시 이름 |
|---|---|---|
| `demo` | `demo1234` | Demo User |
| `alice` | `alice1234` | Alice |

비밀번호는 DB에 PBKDF2 해시와 랜덤 salt로 저장됩니다. 위 계정은 미션 검증용 공개 테스트 계정이며 실제 서비스 비밀정보가 아닙니다.

## 공개 / 보호 경로 정책

| 경로 | 메서드 | 정책 | 설명 |
|---|---|---|---|
| `/` | GET | 공개 | 홈, 인증 상태에 따라 UI 변화 |
| `/login` | GET/POST | 공개 | 로그인 폼/처리 |
| `/logout` | POST | 공개 처리 | 세션 제거 후 홈 이동 |
| `/health` | GET | 공개 | 헬스 체크 |
| `/app/projects` | GET | 보호 | 내 프로젝트 목록 |
| `/app/projects/new` | GET/POST | 보호 | 프로젝트 생성 |
| `/app/projects/{id}` | GET | 보호 + 소유권 | 관계 데이터(Owner + Tasks) 조회 |
| `/app/projects/{id}/tasks` | POST | 보호 + 소유권 | 할 일 생성 |
| `/app/tasks/{id}/complete` | POST | 보호 + 소유권 | `pending -> done` |
| `/app/tasks/{id}/reopen` | POST | 보호 + 소유권 | `done -> pending` |
| `/app/projects/{id}/delete` | POST | 보호 + 소유권 | 프로젝트/자식 Task cascade 삭제 |

보호 URL을 주소창에 직접 입력해도 `Depends(require_user)`가 로그인 여부를 검사하고 `/login?next=...`로 `303` 리다이렉트합니다. 다른 사용자의 리소스는 `404`로 처리해 존재 여부를 노출하지 않습니다.

## 실행 환경

- Python 3.10 이상
- 검증 환경: Python 3.13.5
- 주요 패키지: FastAPI 0.128.2, Uvicorn 0.48.0, SQLAlchemy 2.0.50, Jinja2 3.1.6

### 1. 가상환경과 설치

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 세션 키 설정

Linux/macOS:

```bash
export SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

Windows PowerShell:

```powershell
$env:SESSION_SECRET = python -c "import secrets; print(secrets.token_urlsafe(32))"
```

생성된 값을 README, 로그, 커밋에 복사하지 마세요.

### 3. 서버 실행

```bash
uvicorn app.main:app --reload
```

브라우저에서 `http://127.0.0.1:8000`에 접속합니다. 기본 DB는 `data/b5_3.db`입니다.

## 자동 테스트

```bash
pytest -q
```

검증 범위:

- 로그인 성공/실패/로그아웃
- 비로그인 직접 보호 URL 접근 차단
- 로그인 전/후 UI 차이
- 3개 모델과 2개 양방향 관계
- 사용자 소유권 차단
- 프로젝트 + Task 관계 데이터 출력
- `pending <-> done` 상태 전이
- cascade 삭제
- 앱 재생성 후 SQLite 데이터 지속

## 구조

```text
app/
├── auth/           # 세션 사용자 판별, Depends 인증/인가
├── models/         # SQLAlchemy ORM 모델
├── repositories/   # SELECT/INSERT/DELETE 등 데이터 접근
├── services/       # 인증, 소유권, 상태 전이 비즈니스 규칙
├── routers/        # HTTP 요청/응답, PRG 리다이렉트
├── templates/      # Jinja2 SSR 화면
├── static/         # CSS
├── db.py
└── main.py
```

상태 전이는 repository가 아니라 service에 둡니다. repository는 저장/조회만 책임지고 `TaskService`가 `pending -> done`, `done -> pending` 규칙과 소유권을 조합합니다.

## 부모/자식 삭제 정책

`User.projects`와 `Project.tasks`에 `cascade="all, delete-orphan"`을 적용했습니다. 이 서비스에서 프로젝트는 사용자 소유 범위를 벗어나 독립적으로 존재하지 않고, Task도 프로젝트 없이 의미가 없기 때문입니다. SQLite 외래키도 `PRAGMA foreign_keys=ON`으로 활성화합니다.

## 학습 문서

- `docs/LEARNING.md` - 인증/인가, Depends, relationship, cascade, 상태 전이 설명
- `docs/ARCHITECTURE.md` - 사용자/개발자 관점 흐름과 확장 질문 답변
- `MISSION-WORK-PACKET.md` - Source/Requirement/Evaluation/Gate 추적
- `evidence/test-results.md` - 실제 자동 테스트 및 런타임 결과
