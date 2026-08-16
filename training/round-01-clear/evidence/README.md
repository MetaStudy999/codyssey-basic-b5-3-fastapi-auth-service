# B5-3 Runtime Evidence Guide

Phase C 실제 수행 결과만 저장합니다. Reference 예상 결과를 실제 PASS처럼 기록하지 않습니다.

## 필수 Evidence

1. Python 3.10+ / 패키지 / 서버 기동
2. 로그인 전 홈 UI
3. 잘못된 계정 로그인 실패
4. 정상 로그인 성공
5. 로그인 후 UI 변화
6. 비로그인 보호 URL 직접 접근 차단/로그인 이동
7. 프로젝트 생성/목록
8. 관계 데이터: 소유자 + 프로젝트 + Task 화면
9. Task 생성
10. Task `진행중 → 완료` 상태 변경 전/후
11. 다시 `완료 → 진행중` 전환
12. 로그아웃
13. 로그아웃 후 보호 URL 재차단
14. `database.db` 생성
15. `inspect_db.py`로 User/Project/Task FK 데이터 확인
16. 프로젝트 구조 확인
17. README 절차 재현

## 권장 이름

```text
01-runtime.txt
02-home-logged-out.png
03-login-fail.png
04-login-success.png
05-home-logged-in.png
06-protected-direct-access.txt
07-project-created.png
08-relationship-view.png
09-task-created.png
10-task-before.png
11-task-after.png
12-logout.png
13-protected-after-logout.txt
14-db-inspection.txt
15-project-tree.txt
```

## Secret

`SESSION_SECRET` 실제 값은 Evidence, GitHub, 채팅, 로그에 넣지 않습니다. 테스트 계정 `demo/demo1234`는 공식 README 공개 요구를 위해 만든 로컬 학습용 계정이며 실제 credential이 아닙니다.
