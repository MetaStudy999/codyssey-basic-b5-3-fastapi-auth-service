# B5-3 Evaluation Q&A

## 인증과 인가가 `Depends`에서 어떻게 연결되나요?

로그인 성공 시 `request.session["username"]`에 사용자를 기록합니다. 보호 Router는 `Depends(require_username)`을 선언하고, dependency가 session의 username을 확인합니다. 없으면 303 + `/login`으로 차단하고, 있으면 username을 Router에 전달합니다.

## 비로그인 사용자가 URL을 직접 입력해도 왜 차단되나요?

보호 경로 자체에 `Depends(require_username)`이 붙어 있기 때문입니다. 메뉴를 숨기는 UI만으로 보호하지 않고 서버 요청 단계에서 확인합니다.

## 세션 방식을 선택한 이유는?

이 미션은 Jinja2 SSR 브라우저 서비스입니다. 세션 쿠키는 로그인 후 브라우저 요청에 자연스럽게 이어지고, `Depends` 기반 인증 흐름을 입문자가 확인하기 쉽습니다. 분산 환경에서는 서버 세션 저장소 전략 등을 추가 검토해야 한다는 한계가 있습니다.

## 모델 관계는 어떻게 설계했나요?

User 1:N Project, Project 1:N Task입니다. 사용자는 여러 프로젝트를 가질 수 있고 프로젝트는 여러 Task를 갖습니다. `owner/projects`, `project/tasks`를 `back_populates`로 양방향 연결했습니다.

## 양방향 관계에서 주의할 점은?

객체가 서로를 가리키므로 JSON으로 그대로 직렬화할 때 순환 참조나 과도한 데이터 로딩 문제가 생길 수 있습니다. Reference는 Jinja2 화면에 필요한 관계만 사용하고 ORM 객체 전체를 JSON으로 직렬화하지 않습니다.

## 부모 삭제 시 자식 데이터는 어떻게 하나요?

User→Project와 Project→Task에 `cascade="all, delete-orphan"`을 사용했습니다. 부모가 사라졌는데 소속 자식만 남는 데이터 불일치를 피하려는 선택이며 모델 코드 주석에 이유를 기록했습니다.

## 상태 변경 로직은 왜 Service에 있나요?

`Task.is_done = not Task.is_done`은 HTTP 처리보다 도메인 규칙입니다. Router는 요청/Redirect에 집중하고 Service가 상태 전환 규칙을 책임지게 해 역할을 분리했습니다.

## 상태 변경이 단순 CRUD와 다른 점은?

단순히 필드 값을 임의로 쓰는 것이 아니라 현재 비즈니스 상태를 다음 허용 상태로 전환하는 규칙입니다. 향후 상태가 복잡해져도 Service에서 전환 규칙을 관리할 수 있습니다.

## 새로운 관리자 역할을 추가한다면?

현재 공식 범위는 로그인/비로그인 구분만 요구합니다. 확장한다면 User 역할 필드, 인증 dependency의 역할 검사, 서비스 권한 규칙, UI 노출 정책을 함께 수정해야 합니다.

## REST API + Frontend 분리로 바꾸면 인증은 어떻게 달라질까요?

현재는 SSR과 세션 쿠키 중심입니다. 별도 frontend에서는 same-origin 세션/CORS/CSRF 정책을 재설계하거나 JWT 같은 토큰 방식을 선택할 수 있습니다. Domain Service/Repository/Model은 상당 부분 유지하고 Router/응답/인증 전달 방식이 주로 바뀝니다.

## 사용자 수가 커질 때 세션의 장단점은?

브라우저 기반 인증 흐름이 단순하고 서버에서 세션을 통제하기 쉽다는 장점이 있습니다. 여러 서버로 확장하면 공유 세션 저장소나 sticky session 같은 운영 설계가 필요할 수 있습니다. 이 확장은 B5-3 필수 구현 범위가 아닙니다.

## 전체 흐름을 한 문장으로 설명하면?

사용자가 로그인하면 세션이 생성되고, `Depends`가 보호 요청의 인증을 확인한 뒤 Service가 User→Project→Task 관계와 Task 상태 전환을 처리하고, 결과를 Jinja2 화면으로 보여줍니다.
