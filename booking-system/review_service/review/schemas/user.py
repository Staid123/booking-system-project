from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    username: str
    email: EmailStr
    active: bool = True
    admin: bool = False