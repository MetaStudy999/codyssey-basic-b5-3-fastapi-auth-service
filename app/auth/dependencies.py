from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


class LoginRequired(Exception):
    def __init__(self, next_path: str = "/app/projects") -> None:
        self.next_path = next_path


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    user = UserRepository.get_by_id(db, int(user_id))
    if user is None:
        request.session.clear()
    return user


def require_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = get_optional_user(request, db)
    if user is None:
        raise LoginRequired(request.url.path)
    return user
