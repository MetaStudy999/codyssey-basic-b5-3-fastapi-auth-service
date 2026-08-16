from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth.dependencies import authenticate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    if request.session.get("username"):
        return RedirectResponse(url="/app/projects", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None, "current_user": None},
    )


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not authenticate(username, password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "아이디 또는 비밀번호가 올바르지 않습니다.", "current_user": None},
            status_code=401,
        )

    request.session["username"] = username
    return RedirectResponse(url="/app/projects", status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
