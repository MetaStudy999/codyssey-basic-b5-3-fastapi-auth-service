from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.services.errors import InvalidTransitionError, NotFoundError
from app.services.project_service import ProjectService


class TaskService:
    @staticmethod
    def create_task(db: Session, user: User, project_id: int, title: str) -> Task:
        project = ProjectService.get_project(db, user, project_id)
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("할 일 제목을 입력하세요.")
        return TaskRepository.create(db, project_id=project.id, title=clean_title)

    @staticmethod
    def _owned_task(db: Session, user: User, task_id: int) -> Task:
        task = TaskRepository.get_for_owner(db, task_id, user.id)
        if not task:
            raise NotFoundError("할 일을 찾을 수 없습니다.")
        return task

    @staticmethod
    def complete_task(db: Session, user: User, task_id: int) -> Task:
        task = TaskService._owned_task(db, user, task_id)
        if task.status != "pending":
            raise InvalidTransitionError("이미 완료된 할 일입니다.")
        task.status = "done"
        return TaskRepository.save(db, task)

    @staticmethod
    def reopen_task(db: Session, user: User, task_id: int) -> Task:
        task = TaskService._owned_task(db, user, task_id)
        if task.status != "done":
            raise InvalidTransitionError("진행 중인 할 일은 다시 열 수 없습니다.")
        task.status = "pending"
        return TaskRepository.save(db, task)
