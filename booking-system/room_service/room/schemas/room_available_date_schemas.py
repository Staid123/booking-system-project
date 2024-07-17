from pydantic import BaseModel, ConfigDict
from datetime import date


class RoomAvailableDateBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    room_id: int
    date: date


class RoomAvailableDateIn(RoomAvailableDateBase):
    pass


class RoomAvailableDate(RoomAvailableDateIn):
    id: int


class RoomAvailableDateOut(RoomAvailableDate):
    pass
    