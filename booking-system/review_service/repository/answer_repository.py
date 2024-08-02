from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from review.models import Answer
from review.schemas.reviews_answers_schemas import AnswerIn, AnswerUpdate
from database.database import Session


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_answers():
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


class AnswerRepository(AbstractRepository):
    @staticmethod
    def get_answers(
        session: Session,
        **filters
    ) -> list[Answer]:
        skip = filters.pop('skip', 0)
        limit = filters.pop('limit', 10)
        stmt = (
            select(Answer)
            .options(
                joinedload(Answer.review),
            )
            .filter_by(**filters)
            .offset(skip)
            .limit(limit)
            .order_by(Answer.id)
        )
        answers: list[Answer] = session.scalars(stmt).all()
        return answers
    
    @staticmethod
    def create_answer(
        session: Session,
        answer_in: AnswerIn,
        reviewer_id: int,
    ) -> Answer:
        try:
            answer = Answer(**answer_in.model_dump(), reviewer_id=reviewer_id)
            session.add(answer)
            session.commit()
            return answer
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add new answer"
            )    

    @staticmethod
    def update_answer(
        session: Session,
        answer_update: AnswerUpdate,
        answer_id: int
    ) -> Answer:
        answer: Answer = session.get(Answer, answer_id)
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Answer not found"
            )
        try:
            for name, value in answer_update.model_dump(exclude_unset=True).items():
                setattr(answer, name, value)
            session.commit()
            answer_with_review = (
                session.query(Answer)
                .filter_by(id=answer_id)
                .options(
                    joinedload(Answer.review),
                )
            ).first()
            return answer_with_review
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not update answer"
            )
        
    @staticmethod
    def delete_answer(
        session: Session,
        answer_id: int
    ) -> None:
        try:
            answer: Answer = session.get(Answer, answer_id)
            session.delete(answer)
            session.commit()
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not delete answer"
            )

# Зависимость для получения репозитория
def get_answer_repository() -> AnswerRepository:
    return AnswerRepository