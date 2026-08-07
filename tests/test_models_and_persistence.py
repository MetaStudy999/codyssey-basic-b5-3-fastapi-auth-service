from fastapi.testclient import TestClient
from sqlalchemy import inspect, select

from app.main import create_app
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from tests.conftest import login


def test_three_models_and_two_bidirectional_relationships():
    user_relationships = inspect(User).relationships
    project_relationships = inspect(Project).relationships
    task_relationships = inspect(Task).relationships

    assert "projects" in user_relationships
    assert user_relationships["projects"].back_populates == "owner"
    assert "owner" in project_relationships
    assert project_relationships["owner"].back_populates == "projects"

    assert "tasks" in project_relationships
    assert project_relationships["tasks"].back_populates == "project"
    assert "project" in task_relationships
    assert task_relationships["project"].back_populates == "tasks"


def test_sqlite_persistence_across_app_recreation(db_url):
    app1 = create_app(database_url=db_url, session_secret="one")
    with TestClient(app1) as client:
        login(client)
        response = client.post(
            "/app/projects/new",
            data={"name": "Persisted", "description": "restart-safe"},
            follow_redirects=False,
        )
        assert response.status_code == 303

    app2 = create_app(database_url=db_url, session_secret="two")
    with app2.state.session_factory() as db:
        project = db.scalar(select(Project).where(Project.name == "Persisted"))
        assert project is not None
