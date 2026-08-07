from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.get(User, user_id)

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        return db.scalar(select(User).where(User.username == username))

    @staticmethod
    def create(db: Session, *, username: str, display_name: str, password_salt: str, password_hash: str) -> User:
        user = User(
            username=username,
            display_name=display_name,
            password_salt=password_salt,
            password_hash=password_hash,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
