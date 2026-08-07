from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import require_user
from app.db import get_db
from app.models.user import User
from app.services.errors import InvalidTransitionError, NotFoundError
from app.services.task_service import TaskService


router = APIRouter(prefix="/app", tags=["tasks"])


@router.post("/projects/{project_id}/tasks")
def task_create(
    project_id: int,
    title: str = Form(...),
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    try:
        TaskService.create_task(db, current_user, project_id, title)
    except (NotFoundError, ValueError):
        pass
    return RedirectResponse(f"/app/projects/{project_id}", status_code=303)


@router.post("/tasks/{task_id}/complete")
def task_complete(
    request: Request,
    task_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    try:
        task = TaskService.complete_task(db, current_user, task_id)
    except NotFoundError:
        return RedirectResponse("/app/projects", status_code=303)
    except InvalidTransitionError:
        task = TaskService._owned_task(db, current_user, task_id)
    return RedirectResponse(f"/app/projects/{task.project_id}", status_code=303)


@router.post("/tasks/{task_id}/reopen")
def task_reopen(
    task_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    try:
        task = TaskService.reopen_task(db, current_user, task_id)
    except NotFoundError:
        return RedirectResponse("/app/projects", status_code=303)
    except InvalidTransitionError:
        task = TaskService._owned_task(db, current_user, task_id)
    return RedirectResponse(f"/app/projects/{task.project_id}", status_code=303)
