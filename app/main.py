import os
import secrets
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.auth.dependencies import LoginRequired
from app.db import Base, build_engine, build_session_factory, default_database_url
from app.routers import auth, home, projects, tasks
from app.services.auth_service import AuthService


APP_DIR = Path(__file__).resolve().parent


def create_app(database_url: str | None = None, session_secret: str | None = None) -> FastAPI:
    database_url = database_url or os.getenv("DATABASE_URL") or default_database_url()
    # No secret is committed. If SESSION_SECRET is omitted, an ephemeral key is
    # generated for local single-process learning use; production should set it.
    session_secret = session_secret or os.getenv("SESSION_SECRET") or secrets.token_urlsafe(32)

    engine = build_engine(database_url)
    session_factory = build_session_factory(engine)
    Base.metadata.create_all(engine)
    with session_factory() as db:
        AuthService.seed_demo_users(db)

    app = FastAPI(title="Codyssey B5-3 Project Flow")
    app.state.engine = engine
    app.state.session_factory = session_factory

    app.add_middleware(
        SessionMiddleware,
        secret_key=session_secret,
        same_site="lax",
        https_only=False,
    )

    templates = Jinja2Templates(directory=str(APP_DIR / "templates"))
    home.set_templates(templates)
    auth.set_templates(templates)
    projects.set_templates(templates)

    app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")
    app.include_router(home.router)
    app.include_router(auth.router)
    app.include_router(projects.router)
    app.include_router(tasks.router)

    @app.exception_handler(LoginRequired)
    async def login_required_handler(request: Request, exc: LoginRequired):
        return RedirectResponse(f"/login?next={exc.next_path}", status_code=303)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
