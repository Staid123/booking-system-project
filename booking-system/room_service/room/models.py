from sqlalchemy import (
    TIMESTAMP, 
    ForeignKey, 
    MetaData, 
    func,
    Enum,
    DATE,
    Date
)
from datetime import date, datetime

from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
    relationship
)

from config import settings

from room.enums import RoomType
    


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
    date: Mapped[Date] = mapped_column(DATE)
    
    room = relationship("Room", back_populates="available_dates")


class RoomTypeInfo(Base):
    __tablename__= "room_type_info"

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    name: Mapped[Enum] = mapped_column(Enum(RoomType))

    room = relationship("Room", back_populates="room_types")


class Room(Base):
    number: Mapped[int] = mapped_column(unique=True)
    price: Mapped[int]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    available_dates = relationship("RoomAvailableDate", back_populates="room")
    room_types = relationship("RoomTypeInfo", back_populates="room")


    
