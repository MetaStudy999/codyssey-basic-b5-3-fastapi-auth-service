from sqlalchemy.orm import Session

from app.auth.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


# Public demo account credentials are documented in README as required by the
# mission. Only salted PBKDF2 digests are stored in source/DB seed data here.
DEMO_USER_SEEDS = (
    (
        "demo",
        "Demo User",
        "73ec936d0586f21aa88d0705aeefd049",
        "53a3a1e2107be6f091fa26117071733d26ad991262a59161edef3d8b227b9dfd",
    ),
    (
        "alice",
        "Alice",
        "a11e4fda1ffaa3040cd8a06b9d399837",
        "599b5ac57e32cc5f8f78edd4127d8320a224afb20315ef2b04da753e0b185e6f",
    ),
)


class AuthService:
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> User | None:
        user = UserRepository.get_by_username(db, username.strip())
        if not user:
            return None
        if not verify_password(password, user.password_salt, user.password_hash):
            return None
        return user

    @staticmethod
    def seed_demo_users(db: Session) -> None:
        for username, display_name, password_salt, password_hash in DEMO_USER_SEEDS:
            if UserRepository.get_by_username(db, username):
                continue
            UserRepository.create(
                db,
                username=username,
                display_name=display_name,
                password_salt=password_salt,
                password_hash=password_hash,
            )
