import logging
from typing import Annotated, Any
from service.review_service import ReviewService, get_review_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import db_helper
from review.schemas.reviews_answers_schemas import ReviewOut, ReviewIn, ReviewUpdate
from review.schemas.user import User
from review.utils import get_current_active_user, get_admin_user, get_review_filters

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/review",
    tags=["Review Operations"])


@router.get("/", response_model=list[ReviewOut])
def get_reviews(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    user: Annotated[User, Depends(get_current_active_user)],
    session : Annotated[Session, Depends(db_helper.session_getter)],
    filters: dict[str, Any] = Depends(get_review_filters),
) -> list[ReviewOut]:
    if user:
        return review_service.list_reviews(
            session=session,
            **filters
        )


@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewIn,
    user: Annotated[User, Depends(get_current_active_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> ReviewOut:
    if user:
        return review_service.create_review(
            review_in=review_in,
            session=session,
        )


@router.patch("/{review_id}/", response_model=ReviewOut)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    user: Annotated[User, Depends(get_current_active_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> ReviewOut:
    if user:
        return review_service.update_review(
            review_id=review_id,
            review_update=review_update,
            session=session,
        )


@router.delete("/{review_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> None:
    if user:
        return review_service.delete_review(
            review_id=review_id,
            session=session,
            user=user
        )