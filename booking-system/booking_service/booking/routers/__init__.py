from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from booking.routers.booking_router import router as booking_router
from booking.routers.room_router import router as room_router

# интерфейс для введения токена (который автоматически отправляеятся в заголовки) после логина
http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/hostel", 
    # интерфейс для введения токена (который автоматически отправляеятся в заголовки) после логина
    dependencies=[Depends(http_bearer)]
)

router.include_router(booking_router)
router.include_router(room_router)