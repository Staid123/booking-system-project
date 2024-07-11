from fastapi import HTTPException, status
from jwt import InvalidTokenError


class UserCreateException(Exception):
    def __init__(self, message="Failed to create user"):
        self.message = message
        super().__init__(self.message)


unauthed_user_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid username or password",
)


unactive_user_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="user inactive",
)


token_not_found_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="token invalid (user not found)",
)


invalid_token_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"invalid token error: {InvalidTokenError}",
)