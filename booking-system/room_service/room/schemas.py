from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from room.enums import RoomType


class RoomAvailableDate(BaseModel):
    date: date


class RoomTypeInfo(BaseModel):
    name: "RoomType"


class RoomBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    number: int
    # type: list["RoomTypeInfo"]
    price: int
    description: str
    # available_dates: list[RoomAvailableDate] | None = None


class RoomIn(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime


class RoomUpdate(BaseModel):
    number: int | None = None
    price: int | None = None
    description: str | None = None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    username: str
    email: EmailStr
    active: bool = True
    admin: bool = False


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    
    type: str
    sub: str
    exp: int
    username: str
    email: str
    admin: bool
    jti: bytes
    iat: int
