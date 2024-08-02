from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from review.routers.review_router import router as review_router
from review.routers.answer_router import router as answer_router


router = APIRouter()

router.include_router(review_router)
router.include_router(answer_router)
