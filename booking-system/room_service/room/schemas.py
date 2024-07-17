from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr
from room.enums import RoomStatus, RoomType


class RoomAvailableDate(BaseModel):
    date: date


class RoomTypeInfo(BaseModel):
    name: "RoomType"


class RoomBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    number: int
    type: list["RoomTypeInfo"]
    price: int
    status: RoomStatus = RoomStatus.AVAILABLE
    description: str
    available_dates: list[RoomAvailableDate] | None = None


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
    status: RoomStatus = RoomStatus.AVAILABLE
    description: str | None = None
    available_dates: list[RoomAvailableDate] | None = None


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