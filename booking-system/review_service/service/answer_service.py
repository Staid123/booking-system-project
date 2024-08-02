from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from review.schemas.reviews_answers_schemas import AnswerIn, AnswerOut, AnswerUpdate
from review.schemas.user import User
from review.models import Answer
from repository.answer_repository import AnswerRepository, get_answer_repository
from service.review_service import ReviewService, get_review_service

class AbstractAnswerService(ABC):
    @staticmethod
    @abstractmethod
    def list_answers():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_answer():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def update_answer():
        raise NotImplementedError
    

    @staticmethod
    @abstractmethod
    def delete_answer():
        raise NotImplementedError
    

class AnswerService(AbstractAnswerService):
    @staticmethod
    def list_answers(
        session: Session,
        answer_repository: AnswerRepository = get_answer_repository(),
        **filters,
    ) -> list[AnswerOut]:
        answers: list[Answer] = answer_repository.get_answers(
            session=session,
            **filters
        )
        answers_schemas: list[AnswerOut] = [
            AnswerOut(
                id=answer.id,
                user_id=answer.user_id,
                room_id=answer.room_id,
                review_id=answer.review_id,
                comment=answer.comment,
                reviewer_id=answer.review.id,
                created_at=answer.created_at,
                updated_at=answer.updated_at,
                review=answer.review
            )
            for answer in answers
        ]
        return answers_schemas


    @staticmethod
    def create_answer(
        session: Session,
        answer_in: AnswerIn,
        answer_repository: AnswerRepository = get_answer_repository(),
        review_service: ReviewService = get_review_service()
    ) -> AnswerOut:
        review = review_service.list_reviews(
            session=session,
            id=answer_in.review_id
        )[0]
        print(review.user_id)
        answer: Answer = answer_repository.create_answer(
            session=session,
            answer_in=answer_in,
            reviewer_id=review.user_id
        )
        answer_schema: AnswerOut = AnswerOut(
            id=answer.id,
            user_id=answer.user_id,
            room_id=answer.room_id,
            review_id=answer.review_id,
            comment=answer.comment,
            reviewer_id=review.user_id,
            created_at=answer.created_at,
            updated_at=answer.updated_at,
            review=review
        )
        return answer_schema


    @staticmethod
    def update_answer(
        answer_id: int,
        session: Session,
        answer_update: AnswerUpdate,
        answer_repository: AnswerRepository = get_answer_repository(),
    ) -> AnswerOut:
        answer: Answer = answer_repository.update_answer(
            answer_id=answer_id,
            session=session,
            answer_update=answer_update
        )
        answer_schema: AnswerOut = AnswerOut(
            id=answer.id,
            user_id=answer.user_id,
            room_id=answer.room_id,
            review_id=answer.review_id,
            comment=answer.comment,
            reviewer_id=answer.review.id,
            created_at=answer.created_at,
            updated_at=answer.updated_at,
            review=answer.review
        )
        return answer_schema

    

    @staticmethod
    def delete_answer(
        answer_id: int,
        session: Session,
        user: User,
        answer_repository: AnswerRepository = get_answer_repository()
    ) -> None:
        if user.admin:
            return answer_repository.delete_answer(
                answer_id=answer_id,
                session=session,
            ) 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough rights"
        )


# Зависимость для получения сервиса
def get_answer_service():
    return AnswerService