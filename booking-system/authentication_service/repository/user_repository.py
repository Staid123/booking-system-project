from abc import ABC, abstractmethod

from sqlalchemy import select
from auth.models import User
from database.database import Session
from auth.utils import hash_password
from auth.custom_exceptions import (
    UserCreateException
)
from auth.models import User


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    def create_user():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def get_user_by_email():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def get_all_users():
        raise NotImplementedError


class UserRepository:
    @staticmethod
    def create_user(
        session: Session,
        username: str,
        email: str,
        password_hash: str
    ) -> User:
        try:
            new_user: User = User(
                username=username,
                email=email,
                password_hash=hash_password(password_hash)
            )
            session.add(new_user)
            session.commit()
            return new_user.id
        except Exception:
            raise UserCreateException()
        
    @staticmethod
    def get_user_by_email(session: Session, email: str) -> int:
        stmt = select(User).where(User.email==email)
        user: User = session.scalars(stmt).one_or_none()
        return user
    
    
    @staticmethod
    def get_all_users(session: Session) -> list[User]:
        users: list[User] = session.scalars(User).all()
        return users


# Зависимость для получения репозитория
def get_user_repository() -> UserRepository:
    return UserRepository