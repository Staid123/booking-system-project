import logging

import jwt
import uuid

from datetime import (
    datetime
)


from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordBearer



from pydantic import (
    ValidationError
)

from messaging.consumer import (
    ConsumerAuthorization,
)

from config import settings

from booking.schemas import (
    TokenPayload,
    User
)


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="auth/jwt/login/",
    scheme_name="JWT"
)


def get_current_user(token: str = Depends(reusable_oauth)) -> User:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.auth_jwt.public_key,
            algorithms=[settings.auth_jwt.algorithm]
        )

        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        with ConsumerAuthorization() as consumer_auth:
            _, user = consumer_auth.receive_user_obj_and_token_from_auth_service()
    except Exception as e:
        logging.error(f"Error while processing with ConsumerAuthorization: {e}")

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return User(**user)