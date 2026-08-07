import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def db_url(tmp_path):
    return f"sqlite:///{tmp_path / 'test.db'}"


@pytest.fixture
def app(db_url):
    return create_app(database_url=db_url, session_secret="test-session-secret-not-production")


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


def login(client: TestClient, username: str = "demo", password: str = "demo1234"):
    return client.post(
        "/login",
        data={"username": username, "password": password, "next_path": "/app/projects"},
        follow_redirects=False,
    )
