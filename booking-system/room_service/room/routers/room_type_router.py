import logging
from typing import Annotated, Any
from service.room_type_info_service import RoomTypeService, get_room_type_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import db_helper
from room.schemas.room_type_schemas import RoomTypeInfoIn, RoomTypeInfoOut
from room.schemas.user import User
from room.utils import get_admin_user, get_current_active_user

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/type",
    tags=["Room Type Operations"]
)


@router.get("/{room_id}/", response_model=list[RoomTypeInfoOut])
def get_room_type_info(
    room_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(get_current_active_user)],
    room_type_service: Annotated[RoomTypeService, Depends(get_room_type_service)]
) -> list[RoomTypeInfoOut]:
    if user:
        return room_type_service.get_room_type_info(
            room_id=room_id,
            session=session
        )
    
@router.post("/", response_model=RoomTypeInfoOut, status_code=status.HTTP_201_CREATED)
def create_room_type_info(
    room_type_info_in: RoomTypeInfoIn,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(get_admin_user)],
    room_type_service: Annotated[RoomTypeService, Depends(get_room_type_service)]
) -> RoomTypeInfoOut:
    if user:
        return room_type_service.create_room_type(
           room_type_info_in=room_type_info_in,
           session=session
        )
    
@router.delete("/{room_type_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_type_info(
    room_type_info_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: Annotated[User, Depends(get_admin_user)],
    room_type_service: Annotated[RoomTypeService, Depends(get_room_type_service)]
) -> None:
    if user:
        return room_type_service.delete_room_type(
            room_type_info_id=room_type_info_id,
            session=session
        )
    
