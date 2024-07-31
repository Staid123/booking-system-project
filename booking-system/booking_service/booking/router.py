from datetime import date
import logging
from typing import Annotated
from service.booking_service import BookingService, get_booking_service
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database import db_helper
from booking.schemas import User, BookingIn, BookingOut
from booking.utils import get_current_active_user, get_admin_user, reusable_oauth

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/booking",
    tags=["Booking Operations"]
)


@router.get("/", response_model=list[BookingOut])
def get_bookings(
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
    user: Annotated[User, Depends(get_current_active_user)],
    session : Annotated[Session, Depends(db_helper.session_getter)],
    check_date: date | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1)
) -> list[BookingOut]:
    if user:
        return booking_service.get_bookings_by_date(
            session=session,
            check_date=check_date,
            skip=skip,               
            limit=limit    
        )


@router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingIn,
    user: Annotated[User, Depends(get_current_active_user)],
    token: Annotated[str, Depends(reusable_oauth)],
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> BookingOut:
    if user:
        return booking_service.create_booking(
            booking_in=booking_in,
            session=session,
            user=user,
            token=token
        )


@router.delete("/{booking_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    token: Annotated[str, Depends(reusable_oauth)],
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> None:
    if user:
        return booking_service.delete_booking(
            booking_id=booking_id,
            session=session,
            token=token
        )