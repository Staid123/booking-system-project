import logging
from typing import Annotated, Any
from service.answer_service import AnswerService, get_answer_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import db_helper
from review.schemas.reviews_answers_schemas import AnswerOut, AnswerIn, AnswerUpdate
from review.schemas.user import User
from review.utils import get_current_active_user, get_answer_filters

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/answer",
    tags=["Answer Operations"])


@router.get("/", response_model=list[AnswerOut])
def get_answers(
    answer_service: Annotated[AnswerService, Depends(get_answer_service)],
    user: Annotated[User, Depends(get_current_active_user)],
    session : Annotated[Session, Depends(db_helper.session_getter)],
    filters: dict[str, Any] = Depends(get_answer_filters),
) -> list[AnswerOut]:
    if user:
        return answer_service.list_answers(
            session=session,
            **filters
        )


@router.post("/", response_model=AnswerOut, status_code=status.HTTP_201_CREATED)
def create_answer(
    answer_in: AnswerIn,
    user: Annotated[User, Depends(get_current_active_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> AnswerOut:
    if user:
        return answer_service.create_answer(
            answer_in=answer_in,
            session=session,
        )


@router.patch("/{answer_id}/", response_model=AnswerOut)
def update_answer(
    answer_id: int,
    answer_update: AnswerUpdate,
    user: Annotated[User, Depends(get_current_active_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> AnswerOut:
    if user:
        return answer_service.update_answer(
            answer_id=answer_id,
            answer_update=answer_update,
            session=session,
        )


@router.delete("/{answer_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    answer_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    answer_service: Annotated[AnswerService, Depends(get_answer_service)],
    session: Annotated[Session, Depends(db_helper.session_getter)]
) -> None:
    if user:
        return answer_service.delete_answer(
            answer_id=answer_id,
            session=session,
            user=user
        )