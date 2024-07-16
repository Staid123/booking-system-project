from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from booking.schemas import RoomIn, RoomOut, RoomUpdate, User
from booking.models import Room
from repository.room_repository import RoomRepository, get_room_repository

class AbstractRoomService(ABC):
    @staticmethod
    @abstractmethod
    def list_rooms():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_room():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def update_room():
        raise NotImplementedError
    

class RoomService(AbstractRoomService):
    @staticmethod
    def list_rooms(
        session: Session,
        room_repository: RoomRepository = get_room_repository(),
        **filters,
    ) -> list[RoomOut]:
        rooms: list[Room] = room_repository.get_rooms(
            session=session,
            **filters
        )
        rooms_schemas = [RoomOut.model_validate(room, from_attributes=True) for room in rooms]
        return rooms_schemas


    @staticmethod
    def create_room(
        session: Session,
        room_in: RoomIn,
        user: User,
        room_repository: RoomRepository = get_room_repository(),
    ) -> RoomOut:
        if user.active and user.admin:
            room: Room = room_repository.create_room(
                session=session,
                room_in=room_in
            )
            return RoomOut.model_validate(obj=room, from_attributes=True)
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Not enough rights"
        )

    @staticmethod
    def update_room(
        room_id: int,
        session: Session,
        room_update: RoomUpdate,
        user: User,
        room_repository: RoomRepository = get_room_repository(),
    ) -> RoomOut:
        if user.active and user.admin:
            room: Room = room_repository.update_room(
                room_id=room_id,
                session=session,
                room_update=room_update
            )
            return RoomOut.model_validate(obj=room, from_attributes=True)
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Not enough rights"
        )

# Зависимость для получения сервиса
def get_room_service():
    return RoomService