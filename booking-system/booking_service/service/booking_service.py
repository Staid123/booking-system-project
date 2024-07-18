from abc import ABC, abstractmethod
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from booking.schemas import BookingIn, BookingOut, BookingUpdate
from booking.models import Booking
from repository.booking_repository import BookingRepository, get_booking_repository


class AbstractBookingService(ABC):
    @staticmethod
    @abstractmethod
    def get_bookings_by_date():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_booking():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def update_booking():
        raise NotImplementedError
    

    @staticmethod
    @abstractmethod
    def delete_booking():
        raise NotImplementedError
    

class BookingService(AbstractBookingService):
    @staticmethod
    def get_bookings_by_date(
        session: Session,
        booking_repository: BookingRepository = get_booking_repository(),
        check_date: date | None = None,
    ) -> list[BookingOut]:
        pass
        bookings: list[Booking] = booking_repository.get_bookings_by_date(
            session=session,
            check_date=check_date
        )
        bookings_schemas: list[BookingOut] = [BookingOut.model_validate(booking, from_attributes=True) for booking in bookings]
        return bookings_schemas


    @staticmethod
    def create_booking(
        session: Session,
        booking_in: BookingIn,
        booking_repository: BookingRepository = get_booking_repository(),
    ) -> BookingOut:
        pass
        # room: Room = room_repository.create_room(
        #     session=session,
        #     room_in=room_in
        # )
        # return RoomOut.model_validate(obj=room, from_attributes=True)


    @staticmethod
    def update_booking(
        booking_id: int,
        session: Session,
        booking_update: BookingUpdate,
        booking_repository: BookingRepository = get_booking_repository(),
    ) -> BookingOut:
        pass
        # room: Room = room_repository.update_room(
        #     room_id=room_id,
        #     session=session,
        #     room_update=room_update
        # )
        # return RoomOut.model_validate(obj=room, from_attributes=True)


    @staticmethod
    def delete_booking(
        booking_id: int,
        session: Session,
        booking_repository: BookingRepository = get_booking_repository(),
    ) -> None:
        pass
        # return room_repository.delete_room(
        #     room_id=room_id,
        #     session=session,
        # ) 


# Зависимость для получения сервиса
def get_booking_service() -> BookingService:
    return BookingService