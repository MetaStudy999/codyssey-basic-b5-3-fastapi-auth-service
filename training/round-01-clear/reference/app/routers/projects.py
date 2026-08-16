from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import require_username
from app.database import get_db
from app.services.project_service import ProjectService, ValidationError

router = APIRouter(prefix="/app")
templates = Jinja2Templates(directory="app/templates")
service = ProjectService()


@router.get("/projects", response_class=HTMLResponse)
def project_list(
    request: Request,
    username: str = Depends(require_username),
    db: Session = Depends(get_db),
):
    user, projects = service.list_projects(db, username)
    return templates.TemplateResponse(
        request=request,
        name="projects/list.html",
        context={"current_user": user.username, "projects": projects},
    )


@router.get("/projects/new", response_class=HTMLResponse)
def project_form(request: Request, username: str = Depends(require_username)):
    return templates.TemplateResponse(
        request=request,
        name="projects/new.html",
        context={"current_user": username, "error": None},
    )


@router.post("/projects")
def create_project(
    request: Request,
    name: str = Form(...),
    username: str = Depends(require_username),
    db: Session = Depends(get_db),
):
    try:
        project = service.create_project(db, username, name)
    except ValidationError as exc:
        return templates.TemplateResponse(
            request=request,
            name="projects/new.html",
            context={"current_user": username, "error": str(exc)},
            status_code=400,
        )
    return RedirectResponse(url=f"/app/projects/{project.id}", status_code=303)


@router.get("/projects/{project_id}", response_class=HTMLResponse)
def project_detail(
    project_id: int,
    request: Request,
    username: str = Depends(require_username),
    db: Session = Depends(get_db),
):
    project = service.get_project(db, username, project_id)
    if project is None:
        return templates.TemplateResponse(
            request=request,
            name="not_found.html",
            context={"current_user": username, "message": "프로젝트를 찾을 수 없습니다."},
            status_code=404,
        )
    return templates.TemplateResponse(
        request=request,
        name="projects/detail.html",
        context={"current_user": username, "project": project, "error": None},
    )


@router.post("/projects/{project_id}/tasks")
def create_task(
    project_id: int,
    request: Request,
    title: str = Form(...),
    username: str = Depends(require_username),
    db: Session = Depends(get_db),
):
    try:
        service.add_task(db, username, project_id, title)
    except ValidationError as exc:
        project = service.get_project(db, username, project_id)
        if project is None:
            return RedirectResponse(url="/app/projects", status_code=303)
        return templates.TemplateResponse(
            request=request,
            name="projects/detail.html",
            context={"current_user": username, "project": project, "error": str(exc)},
            status_code=400,
        )
    except LookupError:
        return RedirectResponse(url="/app/projects", status_code=303)

    return RedirectResponse(url=f"/app/projects/{project_id}", status_code=303)


@router.post("/tasks/{task_id}/toggle")
def toggle_task(
    task_id: int,
    username: str = Depends(require_username),
    db: Session = Depends(get_db),
):
    try:
        task = service.toggle_task(db, username, task_id)
    except LookupError:
        return RedirectResponse(url="/app/projects", status_code=303)

    return RedirectResponse(url=f"/app/projects/{task.project_id}", status_code=303)
