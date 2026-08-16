from sqlalchemy.orm import Session

from app.models.domain import Project, Task, User


class DomainRepository:
    def get_user_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def ensure_user(self, db: Session, username: str) -> User:
        user = self.get_user_by_username(db, username)
        if user is None:
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def list_projects(self, db: Session, owner_id: int) -> list[Project]:
        return (
            db.query(Project)
            .filter(Project.owner_id == owner_id)
            .order_by(Project.id.desc())
            .all()
        )

    def create_project(self, db: Session, owner_id: int, name: str) -> Project:
        project = Project(owner_id=owner_id, name=name)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def get_project(self, db: Session, owner_id: int, project_id: int) -> Project | None:
        return (
            db.query(Project)
            .filter(Project.id == project_id, Project.owner_id == owner_id)
            .first()
        )

    def create_task(self, db: Session, project_id: int, title: str) -> Task:
        task = Task(project_id=project_id, title=title)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def get_task_for_owner(self, db: Session, owner_id: int, task_id: int) -> Task | None:
        return (
            db.query(Task)
            .join(Project, Task.project_id == Project.id)
            .filter(Task.id == task_id, Project.owner_id == owner_id)
            .first()
        )

    def save_task(self, db: Session, task: Task) -> Task:
        db.commit()
        db.refresh(task)
        return task
