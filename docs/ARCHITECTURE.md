# Architecture & Evaluation Notes

## 사용자 관점

```text
홈
 ↓ 로그인
세션 생성
 ↓
내 프로젝트 목록
 ↓ 프로젝트 생성
프로젝트 상세 + Owner/Task 관계 데이터
 ↓ Task 생성
pending
 ↓ 완료
 done
 ↓ 다시 열기
pending
 ↓ 로그아웃
보호 경로 접근 시 로그인 화면
```

## 개발자 관점

```text
Request
  ↓
Router
  ↓ Depends(require_user)
Auth dependency ──→ UserRepository
  ↓ authenticated User
Service ── ownership / state transition
  ↓
Repository ── SQLAlchemy Session
  ↓
SQLite
  ↑
ORM relationships
  ↑
Jinja2 TemplateResponse / RedirectResponse(PRG)
```

## 계층 분리 기준

| 계층 | 책임 | 넣지 않는 것 |
|---|---|---|
| `auth/` | 세션 사용자 판별, dependency | 도메인 상태 전이 |
| `routers/` | HTTP 파라미터, status/redirect, template | SQL 쿼리 |
| `services/` | 소유권, 검증, 상태 전이 | HTML 렌더링 |
| `repositories/` | DB 조회/저장 | 로그인 UI |
| `models/` | ORM 스키마/관계 | HTTP 처리 |
| `templates/` | 화면 표현 | DB 접근 |

## 소유권 방어

보호 경로는 두 단계로 방어한다.

1. `require_user`: 비로그인 요청 차단
2. `ProjectService` / `TaskRepository`: `owner_id`를 쿼리에 포함해 다른 사용자의 자원 차단

따라서 메뉴 숨김 여부와 무관하게 직접 URL/POST 요청도 서버에서 차단된다.

## 양방향 관계 주의점

`User.projects`와 `Project.owner`를 동시에 무제한 직렬화하면 순환 참조가 생길 수 있다. Jinja2에서는 필요한 방향만 접근하고, REST API로 전환할 때는 Pydantic 응답 모델로 포함 필드를 제한해야 한다. 대량 목록에서 관계를 반복 lazy-load하면 N+1 문제가 생기므로 목록 쿼리는 `selectinload`를 사용한다.
