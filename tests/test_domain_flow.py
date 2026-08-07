from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models.project import Project
from app.models.task import Task
from tests.conftest import login


def _create_project(client: TestClient, name: str = "B5-3 학습") -> int:
    response = client.post(
        "/app/projects/new",
        data={"name": name, "description": "인증과 상태 전이 학습"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    return int(response.headers["location"].rsplit("/", 1)[1])


def test_create_relation_data_and_state_transition(client: TestClient):
    login(client)
    project_id = _create_project(client)

    task_create = client.post(
        f"/app/projects/{project_id}/tasks",
        data={"title": "Depends 인증 테스트"},
        follow_redirects=False,
    )
    assert task_create.status_code == 303

    detail = client.get(f"/app/projects/{project_id}")
    assert detail.status_code == 200
    assert "소유자: Demo User (demo)" in detail.text
    assert "Depends 인증 테스트" in detail.text
    assert "진행 중" in detail.text

    app = client.app
    with app.state.session_factory() as db:
        task = db.scalar(select(Task).where(Task.project_id == project_id))
        task_id = task.id
        assert task.status == "pending"

    complete = client.post(f"/app/tasks/{task_id}/complete", follow_redirects=False)
    assert complete.status_code == 303
    after = client.get(f"/app/projects/{project_id}")
    assert "완료" in after.text

    with app.state.session_factory() as db:
        task = db.get(Task, task_id)
        assert task.status == "done"

    reopen = client.post(f"/app/tasks/{task_id}/reopen", follow_redirects=False)
    assert reopen.status_code == 303
    reopened = client.get(f"/app/projects/{project_id}")
    assert "진행 중" in reopened.text


def test_ownership_is_enforced_server_side(client: TestClient):
    login(client, "demo", "demo1234")
    project_id = _create_project(client, "Demo private")
    client.post("/logout")

    login(client, "alice", "alice1234")
    detail = client.get(f"/app/projects/{project_id}")
    assert detail.status_code == 404
    assert "Demo private" not in detail.text

    task_create = client.post(
        f"/app/projects/{project_id}/tasks",
        data={"title": "침범 시도"},
        follow_redirects=False,
    )
    assert task_create.status_code == 303

    with client.app.state.session_factory() as db:
        project = db.get(Project, project_id)
        assert project is not None
        assert len(project.tasks) == 0


def test_project_delete_cascades_tasks(client: TestClient):
    login(client)
    project_id = _create_project(client, "Cascade")
    client.post(f"/app/projects/{project_id}/tasks", data={"title": "child"})

    with client.app.state.session_factory() as db:
        task_id = db.scalar(select(Task.id).where(Task.project_id == project_id))
        assert task_id is not None

    delete = client.post(f"/app/projects/{project_id}/delete", follow_redirects=False)
    assert delete.status_code == 303

    with client.app.state.session_factory() as db:
        assert db.get(Project, project_id) is None
        assert db.get(Task, task_id) is None


def test_invalid_state_transition_is_rejected_in_service(client: TestClient):
    from app.models.user import User
    from app.services.errors import InvalidTransitionError
    from app.services.task_service import TaskService

    login(client)
    project_id = _create_project(client, "Transition guard")
    client.post(f"/app/projects/{project_id}/tasks", data={"title": "one-way first"})

    with client.app.state.session_factory() as db:
        user = db.scalar(select(User).where(User.username == "demo"))
        task = db.scalar(select(Task).where(Task.project_id == project_id))
        TaskService.complete_task(db, user, task.id)
        try:
            TaskService.complete_task(db, user, task.id)
        except InvalidTransitionError:
            pass
        else:
            raise AssertionError("done -> done transition must be rejected")


def test_cross_user_cannot_change_task_state(client: TestClient):
    login(client, "demo", "demo1234")
    project_id = _create_project(client, "Demo state")
    client.post(f"/app/projects/{project_id}/tasks", data={"title": "private task"})
    with client.app.state.session_factory() as db:
        task_id = db.scalar(select(Task.id).where(Task.project_id == project_id))

    client.post("/logout")
    login(client, "alice", "alice1234")
    response = client.post(f"/app/tasks/{task_id}/complete", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/app/projects"

    with client.app.state.session_factory() as db:
        task = db.get(Task, task_id)
        assert task.status == "pending"
