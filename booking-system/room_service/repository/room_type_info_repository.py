from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from room.schemas.room_type_schemas import RoomTypeInfoIn
from database.database import Session
from room.models import RoomTypeInfo


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_room_available_dates():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def create_room_type():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def delete_room_type():
        raise NotImplementedError


class RoomTypeInfoRepository(AbstractRepository):
    @staticmethod
    def get_room_available_dates(
        room_id: int,
        session: Session,
    ) -> list[RoomTypeInfo]:
        room_types_info: list[RoomTypeInfo] = session.query(RoomTypeInfo).filter_by(room_id=room_id).all()
        return room_types_info
    
    @staticmethod
    def create_room_type(
        room_type_info_in: RoomTypeInfoIn,
        session: Session
    ) -> RoomTypeInfo:
        try:
            room_type_info: RoomTypeInfo = RoomTypeInfo(**room_type_info_in.model_dump())
            session.add(room_type_info)
            session.commit()
            return room_type_info
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add new room type"
            )

    @staticmethod
    def delete_room_type(
        session: Session,
        room_type_info_id: int
    ) -> None:
        try:
            room_type_info: RoomTypeInfo = session.get(RoomTypeInfo, room_type_info_id)
            session.delete(room_type_info)
            session.commit()
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not delete room type"
            )


# Зависимость для получения репозитория
def get_room_type_info_repository() -> RoomTypeInfoRepository:
    return RoomTypeInfoRepository