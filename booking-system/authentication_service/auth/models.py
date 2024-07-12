from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
)



class Base(DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None]
    email: Mapped[str]
    password_hash: Mapped[str]