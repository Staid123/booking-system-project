from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from room.routers.room_available_date_router import router as room_available_date_router
from room.routers.room_type_router import router as room_type_router
from room.routers.room_router import router as room_router


router = APIRouter(
    prefix="/room", 
)

router.include_router(room_available_date_router)
router.include_router(room_type_router)
router.include_router(room_router)