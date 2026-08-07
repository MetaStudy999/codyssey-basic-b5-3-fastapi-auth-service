from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project


class ProjectRepository:
    @staticmethod
    def list_for_owner(db: Session, owner_id: int) -> list[Project]:
        stmt = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .options(selectinload(Project.tasks))
            .order_by(Project.id.desc())
        )
        return list(db.scalars(stmt))

    @staticmethod
    def get_for_owner(db: Session, project_id: int, owner_id: int) -> Project | None:
        stmt = (
            select(Project)
            .where(Project.id == project_id, Project.owner_id == owner_id)
            .options(selectinload(Project.owner), selectinload(Project.tasks))
        )
        return db.scalar(stmt)

    @staticmethod
    def create(db: Session, *, owner_id: int, name: str, description: str) -> Project:
        project = Project(owner_id=owner_id, name=name, description=description)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete(db: Session, project: Project) -> None:
        db.delete(project)
        db.commit()
