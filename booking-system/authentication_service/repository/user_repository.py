from abc import ABC, abstractmethod

from sqlalchemy import select, update
from auth.schemas import UserOut
from database.database import Session
from auth.utils import hash_password
from auth.custom_exceptions import (
    UserCreateException,
    update_ban_status_exception
)
from auth.models import User
from auth.enums import UserAction


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

    @staticmethod
    @abstractmethod
    def update_user_ban_status():
        raise NotImplementedError


class UserRepository:
    @staticmethod
    def create_user(
        session: Session,
        username: str,
        email: str,
        password_hash: str
    ) -> int:
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
    def get_user_by_email(session: Session, email: str) -> User | None:
        stmt = select(User).where(User.email==email)
        user: User = session.scalars(stmt).one_or_none()
        return user
    
    
    @staticmethod
    def get_all_users(
        session: Session,
        skip: int,
        limit: int
    ) -> list[User]:
        stmt = (
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(User.id)
        )
        users: list[User] = session.scalars(stmt).all()
        return users


    @staticmethod
    def update_user_ban_status(
        session: Session,  
        user: UserOut,
        action: UserAction
    ) -> User:
        new_active_status = action == UserAction.UNBAN
        try:
            stmt = (
                    update(User)
                    .values(active=new_active_status)
                    .where(User.email==user.email)
                    .execution_options(synchronize_session="fetch")
                )
            session.scalars(stmt)
            session.commit()
            # Получение обновленного объекта
            updated_user = session.query(User).filter_by(email=user.email).one()
            return updated_user
        except Exception:
            session.rollback()
            raise update_ban_status_exception

        


# Зависимость для получения репозитория
def get_user_repository() -> UserRepository:
    return UserRepository