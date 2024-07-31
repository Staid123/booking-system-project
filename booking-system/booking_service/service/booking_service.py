import json
import httpx
import logging
from abc import ABC, abstractmethod
from datetime import date, timedelta, datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from booking.schemas import BookingIn, BookingOut, User
from booking.models import Booking
from repository.booking_repository import BookingRepository, get_booking_repository
from messaging.producer import ProducerNotification

ROOM_MICROSERVICE_URL = "http://room_service:8002"
ROOM_AVAILABLE_DATE = "room/available_date"

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
    def delete_booking():
        raise NotImplementedError
    

class BookingService(AbstractBookingService):
    @staticmethod
    def get_bookings_by_date(
        session: Session,
        booking_repository: BookingRepository = get_booking_repository(),
        check_date: date | None = None,
        skip: int = 0,
        limit: int = 10
    ) -> list[BookingOut]:
        bookings: list[Booking] = booking_repository.get_bookings_by_date(
            session=session,
            check_date=check_date,
            skip=skip,            
            limit=limit
        )
        bookings_schemas: list[BookingOut] = [BookingOut.model_validate(booking, from_attributes=True) for booking in bookings]
        return bookings_schemas


    @staticmethod
    def create_booking(
        session: Session,
        booking_in: BookingIn,
        token: str,
        user: User,
        booking_repository: BookingRepository = get_booking_repository(),
    ) -> BookingOut:
        with httpx.Client() as client:
            url = f"{ROOM_MICROSERVICE_URL}/{ROOM_AVAILABLE_DATE}/{booking_in.room_id}/"
            headers = {"Authorization": f"Bearer {token}"}
            # Генерим даты от начала до конца бронирования
            booking_dates = [(booking_in.check_in_date + timedelta(days=day)).strftime("%Y-%m-%d") for day in range((booking_in.check_out_date - booking_in.check_in_date).days + 1)]
            logging.info(f"Dates: {booking_dates}")
            try:
                logging.info(f"Connecting to URL: {url} with params: {booking_in.room_id} and headers: {headers}")
                response = client.get(
                    url=url,
                    headers=headers
                )
                response.raise_for_status()
                response_data = response.json()
                room_dates = [room.get('date') for room in response_data]
                logging.info(f"Response data: {response_data}")  # Отладочная информация
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
            except httpx.ConnectError as exc:
                raise HTTPException(status_code=500, detail=f"Connection refused: {str(exc)}")
        # Проверка все ли даты есть в room
        if not all(date in room_dates for date in booking_dates):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not all desired days for booking are available"
        )
        booking: Booking = booking_repository.create_booking(
            session=session,
            booking_in=booking_in
        )
        with httpx.Client() as client:
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{ROOM_MICROSERVICE_URL}/{ROOM_AVAILABLE_DATE}/{booking.room_id}/"
            try:
                response = client.request(
                    method="DELETE",
                    url=url,
                    headers=headers,
                    json={
                        'dates': room_dates
                    }
                )
                if response.status_code == 204:
                    booking_out_schema = BookingOut.model_validate(obj=booking, from_attributes=True)
                    with ProducerNotification() as producer:
                        producer.send_booking_information_to_notification_service(
                            username=user.username, 
                            email=user.email,
                            booking=booking_out_schema
                        )
                    return booking_out_schema
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Can not delete dates from room service"
                )
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
            except httpx.ConnectError as exc:
                raise HTTPException(status_code=500, detail=f"Connection refused: {str(exc)}")
        

    @staticmethod
    def delete_booking(
        booking_id: int,
        token: str,
        session: Session,
        booking_repository: BookingRepository = get_booking_repository(),
    ) -> None:
        booking: Booking = booking_repository.get_booking_by_id(
            session=session,
            booking_id=booking_id
        )
        booking_repository.delete_booking(
            booking_id=booking_id,
            session=session,
        ) 
        with httpx.Client() as client:
            url = f"{ROOM_MICROSERVICE_URL}/{ROOM_AVAILABLE_DATE}/"
            headers = {"Authorization": f"Bearer {token}"}
            # Генерим даты от начала до конца бронирования
            booking_dates = [
                (booking.check_in_date + timedelta(days=day)).strftime("%Y-%m-%d") 
                for day in range((booking.check_out_date - booking.check_in_date).days + 1)
            ]
            try:
                logging.info(f"Connecting to URL: {url} with headers: {headers}")
                for date in booking_dates:
                    date = datetime.strptime(date, "%Y-%m-%d")
                    if date > datetime.now():
                        response = client.post(
                            url=url,
                            headers=headers,
                            json={
                                'room_id': booking.room_id,
                                'date': date.date().isoformat()
                            }
                        )
                        if response.status_code != 201:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Can not create room available date while deleting booking"
                            )
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
            except httpx.ConnectError as exc:
                raise HTTPException(status_code=500, detail=f"Connection refused: {str(exc)}")


# Зависимость для получения сервиса
def get_booking_service() -> BookingService:
    return BookingService
                
