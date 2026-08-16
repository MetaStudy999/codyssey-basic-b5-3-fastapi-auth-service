# B5-3 R01 Environment

## Golden Path

Python 3.10+ 로컬 가상환경 + FastAPI/Uvicorn + SQLite + 세션 기반 인증을 사용합니다.

## Runtime 환경 변수

서버 시작 전에 아래 변수를 **로컬 셸에서만** 설정합니다.

```bash
export SESSION_SECRET='충분히_긴_임의값'
```

실제 값은 GitHub, 채팅, 로그, Evidence에 저장하지 않습니다.

## 파일 역할

- `setup.sh`: 가상환경/의존성 설치 재현 보조
- `verify.sh`: Reference 구조/문법/인증·관계·상태변경 정적 검증
- `inspect_db.py`: User/Project/Task 관계 데이터 직접 확인
- `reset.sh`: 현재 B5-3 R01이 만든 `.venv`, SQLite DB, cache만 제거

## 서버 실행

```bash
cd training/round-01-clear/reference
source .venv/bin/activate
export SESSION_SECRET='로컬값'
uvicorn app.main:app --reload
```

브라우저는 `http://localhost:8000`을 사용합니다.
