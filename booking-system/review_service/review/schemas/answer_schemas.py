from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .review_schemas import ReviewBase


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
    created_at: datetime
    updated_at: datetime
    review: "ReviewBase"


class AnswerUpdate(BaseModel):
    comment: str