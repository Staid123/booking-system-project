from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AnswerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    room_id: int
    review_id: int
    comment: str


class AnswerIn(AnswerBase):
    pass


class AnswerOut(AnswerIn):
    id: int
    reviewer_id: int
    created_at: datetime
    updated_at: datetime
    review: "ReviewBase"


class AnswerUpdate(BaseModel):
    comment: str


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

    answers: list[AnswerBase | None] = []


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None