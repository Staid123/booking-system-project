from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str