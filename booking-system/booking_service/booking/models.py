from datetime import date, timedelta
from typing import TYPE_CHECKING
from sqlalchemy import (
    JSON,
    TIMESTAMP, 
    ForeignKey, 
    MetaData, 
    UniqueConstraint, 
    func
)
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr
)

from sqlalchemy.ext.hybrid import hybrid_property

from config import settings

if TYPE_CHECKING:
    from booking.enums import (
        RoomType, 
        RoomStatus, 
        BookingStatus
    )


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    

class Room(Base):
    number: Mapped[int] = mapped_column(unique=True)
    type: Mapped[list["RoomType"]]
    price: Mapped[int]
    status: Mapped["RoomStatus"]
    description: Mapped[str]
    available_dates: Mapped[list[date] | None]
    created_at: Mapped[date] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[date] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Booking(Base):
    room_number: Mapped[int] = mapped_column(ForeignKey("room.number"), unique=True)
    guest_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    check_in_date: Mapped[date]
    check_out_date: Mapped[date]
    status: Mapped["BookingStatus"]
    room: Mapped["Room"]
    dates: Mapped[list[date]]

    @hybrid_property
    def date_range(self):
        return [self.check_in_date + timedelta(days=day) for day in range((self.check_out_date - self.check_in_date).days + 1)]

    @date_range.setter
    def date_range(self, value):
        self.dates = value

    def __init__(self, guest_id, room_id, check_in_date, check_out_date, status):
        self.guest_id = guest_id
        self.room_id = room_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = status
        self.dates = self.date_range



    
