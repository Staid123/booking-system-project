import logging
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from auth.utils import (
    validate_password,
    decode_jwt
)

from auth.schemas import UserSchema

from auth.custom_exceptions import (
    unactive_user_exception,
    unauthed_user_exception,
    invalid_token_type_exception,
    token_not_found_exception,
    invalid_token_error
)

from auth.actions import (
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
)


# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


# интерфейс для введения имени и пароля, а затем автоматическое получение токена и отправка его в заголовки
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login/",
)


# Проверка, что юзер зарегистрирован
def validate_auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Get user by username
    if not (user := UserService.get_user_by_username(form_data.username)):
        raise unauthed_user_exception

    if not validate_password(
        password=form_data.password,
        hashed_password=user.password,
    ):
        logger.warning(f"Login attempt failed. Incorrect password for user '{form_data.username}'.")
        raise unauthed_user_exception

    if not user.active:
        raise unactive_user_exception
    
    logger.info(f"Login attempt with username: {user.username}")
    return user


# Проверка типа токена
def validate_token_type(
    payload: dict, 
    token_type: str
) -> bool:
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise invalid_token_type_exception


# Получение информации с токена 
def get_current_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise invalid_token_error
    return payload


# Получение пользователя по полю sub из токена
def get_user_by_token_sub(
    payload: dict,
) -> UserSchema:
    email: str | None = payload.get("sub")
    if user := UserService.get_user_by_email(email):
        return user
    raise token_not_found_exception


# фабрика для создания функций (вводится тип токена, который ожидается)
def get_auth_user_from_token_of_type(token_type: str):
    # Функция для получения информации с токена 
    def get_auth_user_from_token(
        # получаем токен с заголовков
        payload: Annotated[dict, Depends(get_current_token_payload)]
    ) -> UserSchema:
        # проверяем, совпадает ли введенный токен с токеном в заголовке
        validate_token_type(payload=payload, token_type=token_type)
        # получаем данные по токену
        return get_user_by_token_sub(payload)
    return get_auth_user_from_token


# Проверка, что юзер аутентифицирован для выпуска access token'a
get_current_auth_user = get_auth_user_from_token_of_type(token_type=ACCESS_TOKEN_TYPE)
# Проверка, что юзер аутентифицирован для выпуска refresh token'a
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(token_type=REFRESH_TOKEN_TYPE)


# Проверка, что юзер аутентифицирован + активен
def get_current_active_auth_user(
    user: Annotated[UserSchema, Depends(get_current_auth_user)]
):
    if user.active:
        return user
    raise unactive_user_exception