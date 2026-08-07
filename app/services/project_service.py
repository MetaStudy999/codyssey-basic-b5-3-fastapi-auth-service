from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.services.errors import NotFoundError


class ProjectService:
    @staticmethod
    def list_projects(db: Session, user: User) -> list[Project]:
        return ProjectRepository.list_for_owner(db, user.id)

    @staticmethod
    def get_project(db: Session, user: User, project_id: int) -> Project:
        project = ProjectRepository.get_for_owner(db, project_id, user.id)
        if not project:
            # Ownership is enforced server-side. Returning not-found avoids revealing
            # another user's resource identifier.
            raise NotFoundError("프로젝트를 찾을 수 없습니다.")
        return project

    @staticmethod
    def create_project(db: Session, user: User, name: str, description: str) -> Project:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("프로젝트 이름을 입력하세요.")
        return ProjectRepository.create(
            db,
            owner_id=user.id,
            name=clean_name,
            description=description.strip(),
        )

    @staticmethod
    def delete_project(db: Session, user: User, project_id: int) -> None:
        project = ProjectService.get_project(db, user, project_id)
        ProjectRepository.delete(db, project)
