from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
)

from sqlalchemy import Boolean, LargeBinary



class Base(DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[bytes] = mapped_column(LargeBinary)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default='true')
    admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false')