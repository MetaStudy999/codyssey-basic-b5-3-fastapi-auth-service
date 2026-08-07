from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import get_optional_user
from app.db import get_db
from app.models.user import User
from app.services.auth_service import AuthService


router = APIRouter()
templates: Jinja2Templates | None = None


def set_templates(value: Jinja2Templates) -> None:
    global templates
    templates = value


def _safe_next(next_path: str | None) -> str:
    if not next_path:
        return "/app/projects"
    parsed = urlparse(next_path)
    if parsed.scheme or parsed.netloc or not next_path.startswith("/"):
        return "/app/projects"
    return next_path


@router.get("/login", response_class=HTMLResponse)
def login_form(
    request: Request,
    next: str | None = None,
    current_user: User | None = Depends(get_optional_user),
):
    assert templates is not None
    if current_user:
        return RedirectResponse("/app/projects", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"current_user": None, "error": None, "next_path": _safe_next(next)},
    )


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next_path: str = Form("/app/projects"),
    db: Session = Depends(get_db),
):
    assert templates is not None
    user = AuthService.authenticate(db, username, password)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "current_user": None,
                "error": "아이디 또는 비밀번호가 올바르지 않습니다.",
                "next_path": _safe_next(next_path),
            },
            status_code=400,
        )

    request.session.clear()
    request.session["user_id"] = user.id
    return RedirectResponse(_safe_next(next_path), status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
