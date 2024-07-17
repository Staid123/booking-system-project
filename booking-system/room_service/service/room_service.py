from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from room.schemas.room_schemas import RoomIn, RoomOut, RoomUpdate
from room.schemas.user import User
from room.models import Room
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
    

    @staticmethod
    @abstractmethod
    def delete_room():
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
        room_repository: RoomRepository = get_room_repository(),
    ) -> RoomOut:
        room: Room = room_repository.create_room(
            session=session,
            room_in=room_in
        )
        return RoomOut.model_validate(obj=room, from_attributes=True)


    @staticmethod
    def update_room(
        room_id: int,
        session: Session,
        room_update: RoomUpdate,
        room_repository: RoomRepository = get_room_repository(),
    ) -> RoomOut:
        room: Room = room_repository.update_room(
            room_id=room_id,
            session=session,
            room_update=room_update
        )
        return RoomOut.model_validate(obj=room, from_attributes=True)

    

    @staticmethod
    def delete_room(
        room_id: int,
        session: Session,
        room_repository: RoomRepository = get_room_repository()
    ) -> None:
        return room_repository.delete_room(
            room_id=room_id,
            session=session,
        ) 


# Зависимость для получения сервиса
def get_room_service():
    return RoomService