from abc import ABC, abstractmethod
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from room.schemas.room_available_date_schemas import RoomAvailableDateIn
from database.database import Session
from room.models import RoomAvailableDate


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_room_available_dates():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def create_room_available_date():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def delete_room_available_dates():
        raise NotImplementedError
    

class RoomAvailableDateRepository(AbstractRepository):
    @staticmethod
    def get_room_available_dates(
        room_id: int,
        session: Session,
    ) -> list[RoomAvailableDate]:
        dates: list[RoomAvailableDate] = session.query(RoomAvailableDate).filter_by(room_id=room_id).all()
        return dates


    @staticmethod
    def create_room_available_date(
        session: Session,
        room_available_date_in: RoomAvailableDateIn
    ) -> RoomAvailableDate:
        try:
            room_available_date: RoomAvailableDate = RoomAvailableDate(**room_available_date_in.model_dump())
            session.add(room_available_date)
            session.commit()
            return room_available_date
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add new date"
            )
        
    @staticmethod
    def delete_room_available_dates(
        room_available_dates_dates: list[date],
        session: Session
    ) -> None:
        try:
            for room_available_dates_date in room_available_dates_dates:
                stmt = select(RoomAvailableDate).where(RoomAvailableDate.date == room_available_dates_date)
                room_available_date: RoomAvailableDate = session.scalars(stmt).first()
                session.delete(room_available_date)
            session.commit()
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not delete date"
            )


# Зависимость для получения репозитория
def get_room_available_date_repository() -> RoomAvailableDateRepository:
    return RoomAvailableDateRepository