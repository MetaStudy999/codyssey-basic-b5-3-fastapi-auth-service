from fastapi.testclient import TestClient

from tests.conftest import login


def test_public_home_and_login_state_ui(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "로그인하고 시작하기" in response.text
    assert "님 환영합니다" not in response.text

    assert login(client).status_code == 303
    response = client.get("/")
    assert "Demo User님 환영합니다" in response.text
    assert "로그아웃" in response.text


def test_login_failure_and_logout(client: TestClient):
    failure = client.post(
        "/login",
        data={"username": "demo", "password": "wrong", "next_path": "/app/projects"},
    )
    assert failure.status_code == 400
    assert "올바르지 않습니다" in failure.text

    assert login(client).status_code == 303
    logout = client.post("/logout", follow_redirects=False)
    assert logout.status_code == 303
    protected = client.get("/app/projects", follow_redirects=False)
    assert protected.status_code == 303
    assert protected.headers["location"].startswith("/login")


def test_direct_protected_url_redirects_when_anonymous(client: TestClient):
    response = client.get("/app/projects/999", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login?next=/app/projects/999")
