from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .answer_schemas import AnswerBase


class ReviewBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    room_id: int
    rating: int
    comment: str | None = None


class ReviewIn(ReviewBase):
    pass


class ReviewOut(ReviewIn):
    id: int
    created_at: datetime
    updated_at: datetime

    answers: "AnswerBase"


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None