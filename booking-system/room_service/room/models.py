from datetime import date
from sqlalchemy import (
    TIMESTAMP, 
    ForeignKey, 
    MetaData, 
    func
)
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
    relationship
)

from config import settings

from room.enums import (
    RoomType, 
    RoomStatus, 
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
    
    
class RoomAvailableDate(Base):
    __tablename__= "room_available_date"

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    date: Mapped[date]
    
    room = relationship("Room", back_populates="available_dates")


class RoomTypeInfo(Base):
    __tablename__= "room_type_info"

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    name = Mapped[RoomType]

    room = relationship("Room", back_populates="room_types")


class Room(Base):
    number: Mapped[int] = mapped_column(unique=True)
    price: Mapped[int]
    status: Mapped[RoomStatus]
    description: Mapped[str]
    created_at: Mapped[date] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[date] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    available_dates = relationship("RoomAvailableDate", back_populates="room")
    room_types = relationship("RoomTypeInfo", back_populates="room")


# class Booking(Base):
#     room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
#     guest_id: Mapped[int]
#     check_in_date: Mapped[date]
#     check_out_date: Mapped[date]
#     status: Mapped["BookingStatus"]
#     room = relationship("Room", back_populates="bookings")
    # dates: Mapped[list[date]]

    # @hybrid_property
    # def date_range(self):
    #     return [self.check_in_date + timedelta(days=day) for day in range((self.check_out_date - self.check_in_date).days + 1)]

    # @date_range.setter
    # def date_range(self, value):
    #     self.dates = value

    # def __init__(self, guest_id, room_id, check_in_date, check_out_date, status):
    #     self.guest_id = guest_id
    #     self.room_id = room_id
    #     self.check_in_date = check_in_date
    #     self.check_out_date = check_out_date
    #     self.status = status
    #     self.dates = self.date_range



    
