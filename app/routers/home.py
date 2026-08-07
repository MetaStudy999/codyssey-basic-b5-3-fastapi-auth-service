from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.dependencies import get_optional_user
from app.models.user import User


router = APIRouter()
templates: Jinja2Templates | None = None


def set_templates(value: Jinja2Templates) -> None:
    global templates
    templates = value


@router.get("/", response_class=HTMLResponse)
def home(request: Request, current_user: User | None = Depends(get_optional_user)):
    assert templates is not None
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"current_user": current_user},
    )
