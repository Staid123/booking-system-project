from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from review.models import Review
from review.schemas.reviews_answers_schemas import ReviewIn, ReviewUpdate
from database.database import Session


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_reviews():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_review():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def update_review():
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def delete_review():
        raise NotImplementedError


class ReviewRepository(AbstractRepository):
    @staticmethod
    def get_reviews(
        session: Session,
        **filters
    ) -> list[Review]:
        skip = filters.pop('skip', 0)
        limit = filters.pop('limit', 10)
        stmt = (
            select(Review)
            .options(
                selectinload(Review.answers),
                )
            .filter_by(**filters)
            .offset(skip)
            .limit(limit)
            .order_by(Review.id)
        )
        reviews: list[Review] = session.scalars(stmt).all()
        return reviews
    
    @staticmethod
    def create_review(
        session: Session,
        review_in: ReviewIn
    ) -> Review:
        try:
            review = Review(**review_in.model_dump(exclude_unset=True))
            session.add(review)
            session.commit()
            return review
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add new review"
            )    

    @staticmethod
    def update_review(
        session: Session,
        review_update: ReviewUpdate,
        review_id: int
    ) -> Review:
        review: Review = session.get(Review, review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Review not found"
            )
        try:
            for name, value in review_update.model_dump(exclude_unset=True).items():
                setattr(review, name, value)
            session.commit()
            review_with_answers = (
                session.query(Review)
                .filter_by(id=review_id)
                .options(
                    selectinload(Review.answers),
                )
            ).first()
            return review_with_answers
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not update review"
            )
        
    @staticmethod
    def delete_review(
        session: Session,
        review_id: int
    ) -> None:
        try:
            review: Review = session.get(Review, review_id)
            session.delete(review)
            session.commit()
        except Exception:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not delete review"
            )

# Зависимость для получения репозитория
def get_review_repository() -> ReviewRepository:
    return ReviewRepository