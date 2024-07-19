from sqlalchemy import MetaData, UniqueConstraint
from datetime import date

from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
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
    

class Booking(Base):
    room_id: Mapped[int]
    user_id: Mapped[int]
    check_in_date: Mapped[date]
    check_out_date: Mapped[date]

    __table_args__ = (
        UniqueConstraint('room_id', 'check_in_date', 'check_out_date'),
    )

