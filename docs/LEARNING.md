# B5-3 Learning Guide

## 1. Authentication과 Authorization

- **Authentication(인증)**: "누구인가?"를 확인한다. 이 프로젝트는 로그인 성공 후 `request.session["user_id"]`를 저장한다.
- **Authorization(인가)**: "이 사용자가 이 자원에 접근해도 되는가?"를 확인한다. 로그인 여부는 `require_user`, 프로젝트/할 일 소유권은 service/repository 쿼리에서 `owner_id`로 강제한다.

UI에서 버튼을 숨기는 것만으로는 인가가 아니다. 사용자가 URL을 직접 입력하거나 HTTP 요청을 직접 보내도 서버가 막아야 한다.

## 2. FastAPI Depends 흐름

```text
브라우저 GET /app/projects/7
        ↓
projects.project_detail()
        ↓ Depends(require_user)
require_user()
        ↓ request.session['user_id']
UserRepository.get_by_id()
        ↓
로그인 사용자 반환 / 없으면 LoginRequired
        ↓
ProjectService.get_project(user, project_id)
        ↓ owner_id 조건
자기 프로젝트만 조회
        ↓
Jinja2 TemplateResponse
```

`Depends`를 쓰면 각 보호 라우트가 인증 코드를 복사하지 않고 동일한 검사를 재사용한다.

## 3. 왜 세션인가

Jinja2 SSR에서는 브라우저가 서버 페이지를 요청할 때 쿠키가 자연스럽게 함께 전송된다. 따라서 세션은 작은 학습 서비스에서 흐름이 단순하다. JWT는 REST API와 별도 프론트엔드/모바일 클라이언트에서 장점이 있지만, 토큰 저장·갱신·폐기 전략을 추가해야 한다.

## 4. SQLAlchemy 관계

### User 1:N Project

한 사용자는 여러 Project를 소유할 수 있고, 각 Project는 한 owner만 가진다.

```text
User.projects <---- back_populates ----> Project.owner
```

### Project 1:N Task

한 Project는 여러 Task를 포함하고, 각 Task는 한 Project에 속한다.

```text
Project.tasks <---- back_populates ----> Task.project
```

`back_populates`는 양쪽 객체 관계를 명시적으로 연결한다. 관계를 JSON으로 무작정 직렬화하면 `User -> Project -> User -> ...` 식 순환 참조가 생길 수 있으므로 필요한 필드만 응답/템플릿에 사용해야 한다.

## 5. Cascade 정책

`delete-orphan`은 부모와 생명주기를 공유하는 자식에 적합하다. Project가 사라졌는데 Task만 남으면 이 도메인에서는 의미가 없기 때문에 Project 삭제 시 Task도 삭제한다.

반대로 회계 기록처럼 부모가 삭제되어도 보존해야 하는 데이터라면 cascade 삭제를 선택하면 안 된다.

## 6. CRUD와 State Transition 차이

CRUD는 "값을 저장/조회/수정/삭제"하는 일반 동작이다. 상태 전이는 **현재 상태와 허용 규칙**을 검사한다.

이 프로젝트의 `TaskService`는:

- `pending -> done`: 허용
- `done -> pending`: 허용
- `done -> done`: 거부
- `pending -> pending` 재열기: 거부

따라서 상태 변경은 repository가 아니라 service에 둔다. repository가 도메인 규칙까지 알면 데이터 접근과 비즈니스 규칙이 섞여 테스트/변경이 어려워진다.

## 7. 새로운 관리자 역할을 추가한다면

1. `User`에 role 컬럼 또는 별도 Role 모델을 설계한다.
2. `require_user`는 인증만 유지하고, `require_admin` 같은 별도 dependency를 추가한다.
3. service에서 일반 사용자 소유권 규칙과 관리자 예외 규칙을 명시한다.
4. 템플릿은 역할에 따라 메뉴를 다르게 보여주되, 최종 강제는 서버 dependency/service에서 한다.

## 8. REST API + 분리 프론트엔드로 바꾼다면

SSR 리다이렉트 대신 API는 보통 `401 Unauthorized`/`403 Forbidden` JSON을 반환한다. 세션 쿠키를 계속 사용할 수도 있지만 CORS/CSRF 정책이 중요해진다. JWT를 선택하면 프론트엔드가 `Authorization: Bearer ...`로 토큰을 보내고, 만료/재발급/로그아웃 전략을 별도로 설계해야 한다.

## 9. 사용자 수가 크게 늘 때 세션 방식의 장단점

현재 `SessionMiddleware`는 쿠키에 서명된 세션 정보를 담는 방식이라 별도 서버 세션 저장소가 없다. 장점은 단순성과 서버 확장 시 공유 세션 DB가 필요 없다는 점이다. 단점은 쿠키 크기 제한과 민감정보를 세션에 넣으면 안 된다는 점이다. 서버 저장형 세션을 선택한다면 다중 인스턴스에서 Redis 같은 공유 저장소가 필요할 수 있다. JWT 역시 폐기/강제 로그아웃 요구가 커지면 denylist나 짧은 만료/refresh 설계가 필요하다.
