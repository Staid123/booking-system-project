import logging
from typing import Annotated, Any
from service.room_service import RoomService, get_room_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import db_helper
from room.schemas import RoomOut, RoomIn, User, RoomUpdate
from room.utils import get_current_user, get_filters

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
    booking_service: Annotated[RoomService, Depends(get_room_service)],
    session : Annotated[Session, Depends(db_helper.session_getter)],
    filters: dict[str, Any] = Depends(get_filters),
) -> list[RoomOut]:
    return booking_service.list_rooms(
        session=session,
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


@router.patch("/{room_id}/", response_model=RoomOut)
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