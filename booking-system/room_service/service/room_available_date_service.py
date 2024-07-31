from abc import ABC, abstractmethod

from fastapi import HTTPException, status
import httpx
from sqlalchemy.orm import Session
from room.schemas.room_available_date_schemas import DatesToDelete, RoomAvailableDateOut, RoomAvailableDateIn
from room.schemas.user import User
from room.models import RoomAvailableDate
from repository.room_available_date_repository import RoomAvailableDateRepository, get_room_available_date_repository


BOOKING_MICROSERVICE_URL = "http://booking_service:8003"
BOOKING = "booking"

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
        token: str,
        room_available_date_in: RoomAvailableDateIn,
        room_available_date_repository: RoomAvailableDateRepository = get_room_available_date_repository(),
    ) -> RoomAvailableDateOut:
        with httpx.Client() as client:
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{BOOKING_MICROSERVICE_URL}/{BOOKING}/"
            try:
                response = client.get(
                    url=url,
                    headers=headers,
                    params={
                        'check_date': room_available_date_in.date
                    }
                )
                response_data = response.json()
                print(response_data)
                if response_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="The room is already booked for this date."
                    )
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
            except httpx.ConnectError as exc:
                raise HTTPException(status_code=500, detail=f"Connection refused: {str(exc)}")
        room_available_date: RoomAvailableDate = room_available_date_repository.create_room_available_date(
            session=session,
            room_available_date_in=room_available_date_in
        )
        room_available_date_schema: RoomAvailableDateOut = RoomAvailableDateOut.model_validate(room_available_date, from_attributes=True)
        return room_available_date_schema


    @staticmethod
    def delete_room_available_dates(
        room_id: int,
        room_available_dates_dates: DatesToDelete,
        session: Session,
        room_available_date_repository: RoomAvailableDateRepository = get_room_available_date_repository(),
    ) -> None:
        return room_available_date_repository.delete_room_available_dates(
            room_available_dates_dates=room_available_dates_dates,
            session=session,
            room_id=room_id
        )


# Зависимость для получения сервиса
def get_room_available_date_service():
    return RoomAvailableDateService