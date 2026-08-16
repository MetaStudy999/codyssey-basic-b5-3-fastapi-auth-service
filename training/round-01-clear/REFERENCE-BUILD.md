# B5-3 R01 — Reference Build

## Source of Truth

1. `b5-3-mission.pdf`
2. `b5-3-mission.md`
3. `b5-3-evaluation.md`

## Reference 주제

**프로젝트 할 일 관리 서비스**

- User 1:N Project
- Project 1:N Task
- Task 상태 `진행중 ↔ 완료`
- 세션 기반 로그인/로그아웃
- 보호 경로는 `Depends(require_username)`으로 차단

## 인증 선택

공식 방식 A인 **세션 기반 인증**을 선택합니다.

- `SessionMiddleware`
- `SESSION_SECRET`은 환경 변수로만 주입
- 테스트 계정은 공식 요구에 따라 README에 공개하는 로컬 학습용 계정 사용

## Reference 구조

```text
training/round-01-clear/
├── REFERENCE-BUILD.md
├── REFERENCE-STATUS.md
├── BEGINNER-GUIDE.md
├── CHECKLIST.md
├── reference/
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── auth/dependencies.py
│       ├── routers/{home,auth,projects}.py
│       ├── services/project_service.py
│       ├── repositories/domain_repository.py
│       ├── models/domain.py
│       └── templates/...
├── environment/
│   ├── README.md
│   ├── setup.sh
│   ├── verify.sh
│   ├── reset.sh
│   └── inspect_db.py
├── docs/
└── evidence/
```

## 필수 요구 대응

### 인증/인가

- 로그인 성공: session에 username 저장
- 로그인 실패: 401 + 화면 오류 문구
- 로그아웃: session clear
- 보호 경로 직접 입력: `Depends(require_username)`에서 303 + `/login`
- 로그인 전/후 메뉴/환영문구 변화

### 모델/관계

- User, Project, Task 3모델
- User↔Project, Project↔Task 두 1:N 관계
- `relationship(back_populates=...)` 양방향
- 부모 삭제 정책은 `cascade="all, delete-orphan"`로 코드 주석에 이유 기록

### 상태 변경

`ProjectService.toggle_task()`가 `Task.is_done`을 반전합니다. 상태 규칙을 Router가 아니라 Service에 둡니다.

### 데이터/SSR

- SQLite + SQLAlchemy ORM
- 관계 데이터 DB 조회
- Jinja2 SSR

## 의도적으로 하지 않는 것

공식 보너스 또는 불필요한 범위는 Phase A 필수 기준본에서 제외합니다.

- 회원가입/비밀번호 해싱
- OAuth2 소셜 로그인
- 다단계 RBAC
- 외부 배포
- 검색/필터

## Runtime 분리

Reference 구현/검증 설계가 있어도 실제 로그인·직접 URL 차단·관계 화면·상태 토글·DB/Evidence는 Phase C에서만 PASS 처리합니다.
