from typing import Annotated, Any, Optional

import jwt

from datetime import (
    date,
    datetime
)

from booking.schemas import User, TokenPayload


from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordBearer



from pydantic import (
    ValidationError
)

from config import settings



reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8001/jwt/auth/login/",
    scheme_name="JWT"
)


def get_current_user(token: str = Depends(reusable_oauth)) -> User:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.auth_jwt.public_key,
            algorithms=[settings.auth_jwt.algorithm]
        )

        token_data: TokenPayload = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: User = User(
        username=token_data.username,
        email=token_data.email,
        admin=token_data.admin
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="User is not active"
    )


def get_admin_user(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if user.admin:
        return user
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Not enough rights"
    )
