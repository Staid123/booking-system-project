import logging
from typing import Annotated
from service.room_service import RoomService, get_room_service
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database import db_helper
from booking.schemas import RoomOut, RoomIn, User, RoomUpdate
from booking.utils import get_current_user


# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/room", 
    tags=["Room Operations"],
)


@router.get("/", response_model=list[RoomOut])
def get_rooms(
    filters: dict,
    booking_service: Annotated[RoomService, Depends(get_room_service)],
    session : Annotated[Session, Depends(db_helper.session_getter)],
    skip: int = Query(default=0, ge=0), 
    limit: int = Query(default=10, ge=1),
) -> list[RoomOut]:
    return booking_service.list_rooms(
        session=session,
        skip=skip,
        limit=limit,
        **filters
    )


@router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(
    room_in: RoomIn,
    user: Annotated[User, Depends(get_current_user)],
    booking_service: Annotated[RoomService, Depends(get_room_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> RoomOut:
    return booking_service.create_room(
        room_in=room_in,
        session=session,
        user=user
    )


@router.update("/{room_id}/", response_model=RoomOut, status_code=status.HTTP_205_RESET_CONTENT)
def update_room(
    room_id: int,
    room_update: RoomUpdate,
    user: Annotated[User, Depends(get_current_user)],
    booking_service: Annotated[RoomService, Depends(get_room_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> RoomOut:
    return booking_service.update_room(
        room_id=room_id,
        room_update=room_update,
        session=session,
        user=user
    )