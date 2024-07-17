from datetime import datetime
from pydantic import BaseModel, ConfigDict
from room.schemas.room_type_schemas import RoomTypeInfo
from room.schemas.room_available_date_schemas import RoomAvailableDate


class RoomBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    number: int
    price: int
    description: str


class RoomIn(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime
    room_types: list[RoomTypeInfo]
    available_dates: list[RoomAvailableDate]
    


class RoomUpdate(BaseModel):
    number: int | None = None
    price: int | None = None
    description: str | None = None