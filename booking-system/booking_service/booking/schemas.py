from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr
from booking.enums import RoomStatus, RoomType


class RoomBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    number: int
    type: list["RoomType"]
    price: int
    status: "RoomStatus"
    description: str
    available_dates: list[date] | None = None


class RoomIn(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int
    created_at: date
    updated_at: date


class RoomUpdate(BaseModel):
    number: int | None = None
    type: list["RoomType"] | None = None
    price: int | None = None
    status: "RoomStatus" | None = None
    description: str | None = None
    available_dates: list[date] | None = None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    username: str
    email: EmailStr
    active: bool
    admin: bool


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    
    sub: str
    exp: int