from sqlalchemy.orm import Session

from app.models.domain import Project, Task, User
from app.repositories.domain_repository import DomainRepository


class ValidationError(ValueError):
    pass


class ProjectService:
    def __init__(self, repository: DomainRepository | None = None) -> None:
        self.repository = repository or DomainRepository()

    def current_user(self, db: Session, username: str) -> User:
        return self.repository.ensure_user(db, username)

    def list_projects(self, db: Session, username: str) -> tuple[User, list[Project]]:
        user = self.current_user(db, username)
        return user, self.repository.list_projects(db, user.id)

    def create_project(self, db: Session, username: str, name: str) -> Project:
        clean_name = name.strip()
        if not clean_name:
            raise ValidationError("프로젝트 이름을 입력해 주세요.")
        user = self.current_user(db, username)
        return self.repository.create_project(db, user.id, clean_name)

    def get_project(self, db: Session, username: str, project_id: int) -> Project | None:
        user = self.current_user(db, username)
        return self.repository.get_project(db, user.id, project_id)

    def add_task(self, db: Session, username: str, project_id: int, title: str) -> Task:
        clean_title = title.strip()
        if not clean_title:
            raise ValidationError("할 일 제목을 입력해 주세요.")
        project = self.get_project(db, username, project_id)
        if project is None:
            raise LookupError("프로젝트를 찾을 수 없습니다.")
        return self.repository.create_task(db, project.id, clean_title)

    def toggle_task(self, db: Session, username: str, task_id: int) -> Task:
        user = self.current_user(db, username)
        task = self.repository.get_task_for_owner(db, user.id, task_id)
        if task is None:
            raise LookupError("할 일을 찾을 수 없습니다.")

        # 상태 변경 규칙은 HTTP Router가 아니라 Service에 둔다.
        task.is_done = not task.is_done
        return self.repository.save_task(db, task)
