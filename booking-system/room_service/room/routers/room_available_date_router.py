from datetime import date
import logging
from typing import Annotated, Any
from service.room_available_date_service import RoomAvailableDateService, get_room_available_date_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import db_helper
from room.schemas.room_available_date_schemas import RoomAvailableDateOut, RoomAvailableDateIn
from room.schemas.user import User
from room.utils import get_current_active_user, get_admin_user

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/available_date",
    tags=["Room Available Date Operations"]
)


@router.get("/{room_id}/", response_model=list[RoomAvailableDateOut])
def get_room_available_dates(
    room_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(db_helper.session_getter)],
    room_available_date_service: Annotated[RoomAvailableDateService, Depends(get_room_available_date_service)]
) -> list[RoomAvailableDateOut]:
    if user:
        return room_available_date_service.get_room_available_dates_by_id(
            room_id=room_id,
            session=session
        )


@router.post("/", response_model=RoomAvailableDateOut, status_code=status.HTTP_201_CREATED)
def create_room_available_date(
    room_available_date_in: RoomAvailableDateIn,
    user: Annotated[User, Depends(get_admin_user)],
    session: Annotated[Session, Depends(db_helper.session_getter)],
    room_available_date_service: Annotated[RoomAvailableDateService, Depends(get_room_available_date_service)]
) -> RoomAvailableDateOut:
    if user:
        return room_available_date_service.create_room_available_date(
            room_available_date_in=room_available_date_in,        
            session=session    
        )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_available_dates(
    room_available_dates_dates: list[date],
    user: Annotated[User, Depends(get_admin_user)],
    session: Annotated[Session, Depends(db_helper.session_getter)],
    room_available_date_service: Annotated[RoomAvailableDateService, Depends(get_room_available_date_service)]
) -> None:
    if user:
        return room_available_date_service.delete_room_available_dates(
            room_available_dates_dates=room_available_dates_dates,
            session=session,
        )

