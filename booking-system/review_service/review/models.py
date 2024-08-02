from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint, 
    ForeignKey, 
    MetaData,
    UniqueConstraint,
    func,
)
from datetime import datetime

from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
    relationship
)

from config import settings

    
class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    

class Review(Base):
    user_id: Mapped[int]
    room_id: Mapped[int]
    rating: Mapped[int]
    comment: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    answers = relationship("Answer", back_populates="review")

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range_check'),
        UniqueConstraint("user_id", "room_id")
    )


class Answer(Base):
    user_id: Mapped[int]
    reviewer_id: Mapped[int]
    room_id: Mapped[int]
    review_id: Mapped[int] = mapped_column(ForeignKey('review.id'))
    comment: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    review: Mapped["Review"] = relationship("Review", back_populates="answers")


    
