from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy import select
from booking.models import Room
from booking.schemas import RoomIn, RoomUpdate
from database.database import Session


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_rooms():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_room():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def update_room():
        raise NotImplementedError
    

class RoomRepository(AbstractRepository):
    @staticmethod
    def get_rooms(
        session: Session,
        skip: int,
        limit: int,
        **filters
    ) -> list[Room]:
        stmt = (
            select(Room)
            .filter_by(**filters)
            .offset(skip)
            .limit(limit)
            .order_by(Room.id)
        )
        users: list[Room] = session.scalars(stmt).all()
        return users
    
    @staticmethod
    def create_room(
        session: Session,
        room_in: RoomIn
    ) -> Room:
        try:
            room = Room(**room_in.model_dump())
            session.add(room)
            session.commit()
            return room
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add new room"
            )    

    @staticmethod
    def update_room(
        session: Session,
        room_update: RoomUpdate,
        room_id: int
    ) -> Room:
        try:
            room: Room = session.get(Room, room_id)
            for name, value in room_update.model_dump(exclude_none=True):
                setattr(room, name, value)
            session.commit()
            return room
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not update room"
            ) 

# Зависимость для получения репозитория
def get_room_repository() -> RoomRepository:
    return RoomRepository