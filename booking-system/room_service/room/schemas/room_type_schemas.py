from pydantic import BaseModel, ConfigDict, field_validator
from room.enums import RoomType


class RoomTypeInfoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    room_id: int
    name: RoomType

    @field_validator('name', mode='before')
    def parse_room_type(cls, value,):
        if isinstance(value, str):
            try:
                return RoomType(value)
            except ValueError:
                raise ValueError(f"Invalid room type: {value}")
        return value

class RoomTypeInfoIn(RoomTypeInfoBase):
    pass


class RoomTypeInfo(RoomTypeInfoBase):
    id: int


class RoomTypeInfoOut(RoomTypeInfo):
    pass