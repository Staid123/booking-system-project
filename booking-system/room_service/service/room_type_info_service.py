from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from room.schemas.room_type_schemas import RoomTypeInfoIn, RoomTypeInfoOut
from room.schemas.user import User
from room.models import RoomAvailableDate, RoomTypeInfo
from repository.room_type_info_repository import RoomTypeInfoRepository, get_room_type_info_repository


class AbstractService(ABC):
    @staticmethod
    @abstractmethod
    def get_room_type_info():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def create_room_type():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def delete_room_type():
        raise NotImplementedError
    

class RoomTypeService(AbstractService):
    @staticmethod
    def get_room_type_info(
        room_id: int,
        session: Session,
        room_type_info_repository: RoomTypeInfoRepository = get_room_type_info_repository(),
    ) -> list[RoomTypeInfoOut]:
        room_types_info: list[RoomAvailableDate] = room_type_info_repository.get_room_type_info(
            session=session,
            room_id=room_id
        )
        room_types_info_schemas: list[RoomTypeInfoOut] = [RoomTypeInfoOut.model_validate(room_type_info, from_attributes=True) for room_type_info in room_types_info]
        return room_types_info_schemas


    @staticmethod
    def create_room_type(
        session: Session,
        room_type_info_in: RoomTypeInfoIn,
        room_type_info_repository: RoomTypeInfoRepository = get_room_type_info_repository(),
    ) -> RoomTypeInfoOut:
        room_type_info: RoomTypeInfo = room_type_info_repository.create_room_type(
            session=session,
            room_type_info_in=room_type_info_in
        )
        room_type_info_schema: RoomTypeInfoOut = RoomTypeInfoOut.model_validate(obj=room_type_info, from_attributes=True)
        return room_type_info_schema

    
    @staticmethod
    def delete_room_type(
        session: Session,
        room_type_info_id: int,
        room_type_info_repository: RoomTypeInfoRepository = get_room_type_info_repository(),
    ) -> None:
        return room_type_info_repository.delete_room_type(
            session=session,
            room_type_info_id=room_type_info_id
        )


# Зависимость для получения сервиса
def get_room_type_service() -> RoomTypeService:
    return RoomTypeService