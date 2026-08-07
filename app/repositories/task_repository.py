from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project
from app.models.task import Task


class TaskRepository:
    @staticmethod
    def get_for_owner(db: Session, task_id: int, owner_id: int) -> Task | None:
        stmt = (
            select(Task)
            .join(Project, Task.project_id == Project.id)
            .where(Task.id == task_id, Project.owner_id == owner_id)
            .options(selectinload(Task.project))
        )
        return db.scalar(stmt)

    @staticmethod
    def create(db: Session, *, project_id: int, title: str) -> Task:
        task = Task(project_id=project_id, title=title, status="pending")
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def save(db: Session, task: Task) -> Task:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
