from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr


class BookingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room_id: int
    user_id: int
    check_in_date: date
    check_out_date: date


class BookingIn(BookingBase):
    pass


class BookingOut(BookingIn):
    id: int


class BookingUpdate(BaseModel):
    room_id: int | None = None
    user_id: int | None = None
    check_in_date: date | None = None
    check_out_date: date | None = None


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    
    type: str
    sub: str
    exp: int
    username: str
    email: str
    admin: bool
    jti: str
    iat: int


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    username: str
    email: EmailStr
    active: bool = True
    admin: bool = False