from abc import ABC, abstractmethod
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from room.schemas.room_available_date_schemas import RoomAvailableDateOut, RoomAvailableDateIn
from room.schemas.user import User
from room.models import RoomAvailableDate
from repository.room_available_date_repository import RoomAvailableDateRepository, get_room_available_date_repository


class AbstractService(ABC):
    @staticmethod
    @abstractmethod
    def get_room_available_dates_by_id():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def create_room_available_date():
        raise NotImplementedError
    

    @staticmethod
    @abstractmethod
    def delete_room_available_dates():
        raise NotImplementedError
    

class RoomAvailableDateService(AbstractService):
    @staticmethod
    def get_room_available_dates_by_id(
        room_id: int,
        session: Session,
        room_available_date_repository: RoomAvailableDateRepository = get_room_available_date_repository(),
    ) -> list[RoomAvailableDateOut]:
        dates: list[RoomAvailableDate] = room_available_date_repository.get_room_available_dates(
            session=session,
            room_id=room_id
        )
        room_available_dates_schemas: list[RoomAvailableDateOut] = [RoomAvailableDateOut.model_validate(date, from_attributes=True) for date in dates]
        return room_available_dates_schemas


    @staticmethod
    def create_room_available_date(
        session: Session,
        room_available_date_in: RoomAvailableDateIn,
        room_available_date_repository: RoomAvailableDateRepository = get_room_available_date_repository(),
    ) -> RoomAvailableDateOut:
        room_available_date: RoomAvailableDate = room_available_date_repository.create_room_available_date(
            session=session,
            room_available_date_in=room_available_date_in
        )
        room_available_date_schema: RoomAvailableDateOut = RoomAvailableDateOut.model_validate(room_available_date, from_attributes=True)
        return room_available_date_schema


    @staticmethod
    def delete_room_available_dates(
        room_available_dates_dates: list[date],
        session: Session,
        room_available_date_repository: RoomAvailableDateRepository = get_room_available_date_repository(),
    ) -> None:
        return room_available_date_repository.delete_room_available_dates(
            room_available_dates_dates=room_available_dates_dates,
            session=session
        )


# Зависимость для получения сервиса
def get_room_available_date_service():
    return RoomAvailableDateService