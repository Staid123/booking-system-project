from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated

from fastapi import Depends

from auth.models import User
from repository.user_repository import (
    UserRepository, 
    get_user_repository
)
from sqlalchemy.orm import Session
from auth.schemas import UserIn, UserOut
from auth.custom_exceptions import (
    UserCreateException, 
    user_not_found_exception,
    not_enough_rights_exception
)

from auth.enums import UserAction


class AbstractUserService(ABC):
    @staticmethod
    @abstractmethod
    def register_user():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def get_user_by_email():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def list_users():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update_user_ban_status_by_email():
        raise NotImplementedError


class UserService(AbstractUserService):
    @staticmethod
    def register_user(
        session: Session, 
        user_in: UserIn,
        user_repository: UserRepository = get_user_repository()
    ) -> int:
        try:
            new_user_id = user_repository.create_user(
                session=session,
                **user_in.model_dump()
            )
            return new_user_id
        except UserCreateException as ex:
            return f"{ex}: failure to create new user"

    @staticmethod
    def get_user_by_email(
        session: Session, 
        email: str,
        user_repository: UserRepository = get_user_repository(),
    ) -> UserOut:
        user: User | None = user_repository.get_user_by_email(
            session=session, 
            email=email
        )
        if user:
            return UserOut.model_validate(obj=user, from_attributes=True)
        return None
    

    @staticmethod
    def list_users(
        session: Session,
        skip: int,
        limit: int,
        user_repository: UserRepository = get_user_repository()
    ) -> list[UserOut]:
        users = user_repository.get_all_users(
            session=session,
            skip=skip,
            limit=limit
        )
        users_schemas = [UserOut.model_validate(user, from_attributes=True) for user in users]
        return users_schemas
    

    @staticmethod
    def update_user_ban_status_by_email(
        session: Session, 
        admin: UserOut, 
        email: str,
        action: UserAction,
        user_repository: UserRepository = get_user_repository(),
    ) -> UserOut:
        # Get user by email
        user: UserOut = UserService.get_user_by_email(
            session=session,
            email=email
        )
        admin: UserOut = UserService.get_user_by_email(
            session=session,
            email=admin.email
        )
        if not admin.admin or user.admin:
            raise not_enough_rights_exception
        if not user:
            raise user_not_found_exception
        user = user_repository.update_user_ban_status(
            session=session,
            user=user,
            action=action
        )
        user_schema = UserOut.model_validate(obj=user, from_attributes=True)
        return {
            "action": action,
            "user": {
                **user_schema.model_dump()
            },
            "at_time": datetime.now(),
            "made_by": {
                **admin.model_dump()
            }
        }


# Зависимость для получения сервиса
def get_user_service():
    return UserService