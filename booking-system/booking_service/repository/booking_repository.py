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
    def get_booking_by_id():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_booking():
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
    def get_booking_by_id(
        session: Session,
        booking_id: int
    ) -> Booking:
        return session.get(Booking, booking_id)


    @staticmethod
    def create_booking(
        session: Session,
        booking_in: BookingIn
    ) -> Booking:
        try:
            booking = Booking(**booking_in.model_dump())
            session.add(booking)
            session.commit()
            return booking
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add new booking"
            )    
        
    @staticmethod
    def delete_booking(
        session: Session,
        booking_id: int
    ) -> None:
        try:
            booking: Booking = session.get(Booking, booking_id)
            session.delete(booking)
            session.commit()
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not delete booking"
            )

# Зависимость для получения репозитория
def get_booking_repository() -> BookingRepository:
    return BookingRepository