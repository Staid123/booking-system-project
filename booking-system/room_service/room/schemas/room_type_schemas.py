from pydantic import BaseModel, ConfigDict
from room.enums import RoomType


class RoomTypeInfoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    room_id: int
    name: RoomType


class RoomTypeInfoIn(RoomTypeInfoBase):
    pass


class RoomTypeInfo(RoomTypeInfoBase):
    id: int


class RoomTypeInfoOut(RoomTypeInfo):
    pass