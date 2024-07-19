from abc import ABC, abstractmethod
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from booking.models import Booking
from booking.schemas import BookingIn, BookingUpdate
from database.database import Session


class AbstractRepository(ABC):
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


class BookingRepository(AbstractRepository):
    @staticmethod
    def get_bookings_by_date(
        session: Session,
        check_date: date | None = None,
        skip: int = 0,
        limit: int = 10
    ) -> list[Booking]:
        if check_date:
            stmt = (
                select(Booking)
                .where(Booking.check_in_date <= check_date, Booking.check_out_date >= check_date)
                .offset(skip)
                .limit(limit)
                .order_by(Booking.id)
            )
        else: 
            stmt = (
                select(Booking)
                .offset(skip)
                .limit(limit)
                .order_by(Booking.id)
            )
        bookings: list[Booking] = session.scalars(stmt).all()
        return bookings
    
    @staticmethod
    def create_booking(
        session: Session,
        booking_in: BookingIn
    ) -> Booking:
        try:
            room = Booking(**booking_in.model_dump())
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
    def update_booking(
        session: Session,
        booking_update: BookingUpdate,
        booking_id: int
    ) -> Booking:
        pass
        # room: Room = session.get(Room, room_id)
        # if not room:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND, 
        #         detail="Room not found"
        #     )
        # try:
        #     for name, value in room_update.model_dump(exclude_unset=True).items():
        #         setattr(room, name, value)
        #     session.commit()
        #     room_with_dates_and_types = (
        #         session.query(Room)
        #         .filter_by(id=room_id)
        #         .options(
        #             selectinload(Room.available_dates),
        #             selectinload(Room.room_types)
        #         )
        #     ).first()
        #     return room_with_dates_and_types
        # except Exception:
        #     session.rollback()
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Can not update room"
        #     )
        
    @staticmethod
    def delete_booking(
        session: Session,
        booking_id: int
    ) -> None:
        pass
        # try:
        #     room: Room = session.get(Room, room_id)
        #     session.delete(room)
        #     session.commit()
        # except Exception:
        #     session.rollback()
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Can not delete room"
        #     )

# Зависимость для получения репозитория
def get_booking_repository() -> BookingRepository:
    return BookingRepository