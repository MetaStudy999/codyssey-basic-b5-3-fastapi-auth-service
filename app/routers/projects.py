from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import require_user
from app.db import get_db
from app.models.user import User
from app.services.errors import NotFoundError
from app.services.project_service import ProjectService


router = APIRouter(prefix="/app/projects", tags=["projects"])
templates: Jinja2Templates | None = None


def set_templates(value: Jinja2Templates) -> None:
    global templates
    templates = value


@router.get("", response_class=HTMLResponse)
def project_list(
    request: Request,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    assert templates is not None
    projects = ProjectService.list_projects(db, current_user)
    return templates.TemplateResponse(
        request=request,
        name="projects/list.html",
        context={"current_user": current_user, "projects": projects},
    )


@router.get("/new", response_class=HTMLResponse)
def project_new(request: Request, current_user: User = Depends(require_user)):
    assert templates is not None
    return templates.TemplateResponse(
        request=request,
        name="projects/new.html",
        context={"current_user": current_user, "error": None},
    )


@router.post("/new")
def project_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    assert templates is not None
    try:
        project = ProjectService.create_project(db, current_user, name, description)
    except ValueError as exc:
        return templates.TemplateResponse(
            request=request,
            name="projects/new.html",
            context={"current_user": current_user, "error": str(exc)},
            status_code=400,
        )
    return RedirectResponse(f"/app/projects/{project.id}", status_code=303)


@router.get("/{project_id}", response_class=HTMLResponse)
def project_detail(
    request: Request,
    project_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    assert templates is not None
    try:
        project = ProjectService.get_project(db, current_user, project_id)
    except NotFoundError:
        return templates.TemplateResponse(
            request=request,
            name="not_found.html",
            context={"current_user": current_user, "message": "프로젝트를 찾을 수 없습니다."},
            status_code=404,
        )
    return templates.TemplateResponse(
        request=request,
        name="projects/detail.html",
        context={"current_user": current_user, "project": project, "error": None},
    )


@router.post("/{project_id}/delete")
def project_delete(
    project_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    try:
        ProjectService.delete_project(db, current_user, project_id)
    except NotFoundError:
        return RedirectResponse("/app/projects", status_code=303)
    return RedirectResponse("/app/projects", status_code=303)
