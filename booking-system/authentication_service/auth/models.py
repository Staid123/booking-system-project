from datetime import (
    datetime,
    timedelta
)

from typing import List

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    relationship

)



class Base(DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str]
    password_hash: Mapped[str]
    sessions: Mapped[List["Session"]] = relationship(back_populates="user", uselist=True)


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    token: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime]
    user: Mapped["User"] = relationship(back_populates="sessions", uselist=False)