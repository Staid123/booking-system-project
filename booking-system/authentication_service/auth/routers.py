import logging

from typing import Annotated

from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status
)

from fastapi.security import (
    HTTPBearer, 
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm
)

from jwt import InvalidTokenError

from .schemas import TokenInfo, UserSchema

from .custom_exceptions import (
    UserCreateException,
    unauthed_user_exception,
    unactive_user_exception,
    token_not_found_exception,
    invalid_token_error,
    invalid_token_type_exception
)

from .utils import (
    validate_password,
    decode_jwt,
)

from .actions import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
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

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login/",
)

router = APIRouter(
    prefix="/jwt", 
    tags=["UserAuth Operations"],
    dependencies=[Depends(http_bearer)]
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


# Проверка, что юзер аутентифицирован
def get_current_auth_user(
    payload: Annotated[dict, Depends(get_current_token_payload)]
) -> UserSchema:
    token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_TYPE:
        raise invalid_token_type_exception
    email: str | None = payload.get("sub")
    if user := UserService.get_user_by_email(email):
        return user
    raise token_not_found_exception



# Проверка, что юзер аутентифицирован + активен
def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise unactive_user_exception


@router.post(
    "/auth/signup", 
    summary="Create new user"
)
def create_user_handler(user_in: UserSchema):
    # Get user by email
    user = UserService.get_user_by_email(user_in.email)

    # If the user exists raise HTTPException
    if user:
        logger.warning(f"Attempted to create a user with an email that already exists: {user_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    try:
        # Create user using repository for user
        user_id = UserService.register_user(user_in)
        logger.info(f"User created successfully: {user_in.username}")
        return {
            "status_code": 200,
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
def login_handler(user: Annotated[UserSchema, Depends(validate_auth_user)]):
    # Create access and refresh token using email
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user.email)

    with ProducerAuthorization() as producer_auth:
        producer_auth.send_user_object_and_token_to_services(access_token, user)

    logger.info(f"User '{user.username}' successfully logged in.")

    # Return access and refresh token
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    user: Annotated[UserSchema, Depends(get_current_active_auth_user)]
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }