from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from review.schemas.reviews_answers_schemas import ReviewIn, ReviewOut, ReviewUpdate
from review.schemas.user import User
from review.models import Review
from repository.review_repository import ReviewRepository, get_review_repository

class AbstractReviewService(ABC):
    @staticmethod
    @abstractmethod
    def list_reviews():
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
    

class ReviewService(AbstractReviewService):
    @staticmethod
    def list_reviews(
        session: Session,
        review_repository: ReviewRepository = get_review_repository(),
        **filters,
    ) -> list[ReviewOut]:
        reviews: list[Review] = review_repository.get_reviews(
            session=session,
            **filters
        )
        reviews_schemas = [ReviewOut.model_validate(review, from_attributes=True) for review in reviews]
        return reviews_schemas


    @staticmethod
    def create_review(
        session: Session,
        review_in: ReviewIn,
        review_repository: ReviewRepository = get_review_repository(),
    ) -> ReviewOut:
        review: Review = review_repository.create_review(
            session=session,
            review_in=review_in
        )
        return ReviewOut.model_validate(obj=review, from_attributes=True)


    @staticmethod
    def update_review(
        review_id: int,
        session: Session,
        review_update: ReviewUpdate,
        review_repository: ReviewRepository = get_review_repository(),
    ) -> ReviewOut:
        review: Review = review_repository.update_review(
            review_id=review_id,
            session=session,
            review_update=review_update
        )
        return ReviewOut.model_validate(obj=review, from_attributes=True)

    

    @staticmethod
    def delete_review(
        review_id: int,
        session: Session,
        user: User,
        review_repository: ReviewRepository = get_review_repository()
    ) -> None:
        if user.admin:
            return review_repository.delete_review(
                review_id=review_id,
                session=session,
            ) 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough rights"
        )


# Зависимость для получения сервиса
def get_review_service():
    return ReviewService