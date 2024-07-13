import logging

from typing import Annotated

from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status
)
from sqlalchemy.orm import Session
from database import db_helper
from fastapi.security import HTTPBearer
from service.user_service import UserService, get_user_service
from auth.schemas import TokenInfo, UserIn, UserOut

from auth.custom_exceptions import UserCreateException

from auth.validation import (
    validate_auth_user,
    get_current_token_payload,
    get_current_active_auth_user,
    get_current_auth_user_for_refresh,
)

from auth.actions import (
    create_access_token, 
    create_refresh_token
)


# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)

# интерфейс для введения токена (который автоматически отправляеятся в заголовки) после логина
http_bearer = HTTPBearer(auto_error=False)


router = APIRouter(
    prefix="/jwt", 
    tags=["UserAuth Operations"],
    # нужно, чтобы на каждый эндпоинт приходил токен автоматически (для этого указан auto_error=True, 
    # чтобы токен не надо было вводить вручную везде)
    dependencies=[Depends(http_bearer)]
)


@router.post(
    "/auth/signup", 
    summary="Create new user"
)
def create_user_handler(
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_in: UserIn
) -> dict:
    # Get user by email
    user: UserOut = user_service.get_user_by_email(
        session=session,
        email=user_in.email
    )

    # If the user exists raise HTTPException
    if user:
        logger.warning(f"Attempted to create a user with an email that already exists: {user_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    try:
        # Create user using repository for user
        user_id = user_service.register_user(
            session=session,
            user_in=user_in
        )
        logger.info(f"User created successfully: {user_in.username}")
        return {
            "user": {
                "user_id": user_id,
                **user_in.model_dump()
                }
            }
    except UserCreateException as ex:
        logger.error(f"Failed to create a new user: {ex}", exc_info=True)
        return f"{ex}: failure to create new user"
    

@router.post(
    "/auth/login", 
    summary="Create access and refresh tokens for user", 
    response_model=TokenInfo
)
def login_handler(user: Annotated[UserIn, Depends(validate_auth_user)]):
    # Create access and refresh token using email
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    # with ProducerAuthorization() as producer_auth:
    #     producer_auth.send_user_object_and_token_to_services(access_token, user)

    logger.info(f"User '{user.username}' successfully logged in.")

    # Return access and refresh token
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/refresh/", 
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary="Create new access token"
)
def auth_refresh_jwt(
    user: Annotated[UserIn, Depends(get_current_auth_user_for_refresh)]
): 
    # можно выпускать еще refresh токен при обновлении access (некоторые так делают)
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token
    )



@router.get(
    "/users/me/", 
    response_model=UserOut,
    summary="Get user info"
)
def auth_user_check_self_info(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    user: Annotated[UserIn, Depends(get_current_active_auth_user)]
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }


@router.get(
    "/users/all/", 
    response_model=list[UserOut],
    summary="Get all users info"
)
def get_all_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)],
    admin: Annotated[UserIn, Depends(get_current_active_auth_user)]
):
    return user_service.list_users(session=session)