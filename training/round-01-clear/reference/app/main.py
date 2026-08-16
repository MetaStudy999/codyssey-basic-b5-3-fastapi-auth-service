import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app.models.domain import Project, Task, User  # noqa: F401 - register ORM tables
from app.routers import auth, home, projects

SESSION_SECRET = os.environ.get("SESSION_SECRET")
if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET environment variable is required")

app = FastAPI(title="B5-3 Project Task Auth Reference")
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=False,  # Localhost R01 runtime. Use HTTPS cookies in real deployment.
)

Base.metadata.create_all(bind=engine)

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(projects.router)
