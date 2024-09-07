from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .odrer import Order


class User(IntIdPkMixin, Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    email: Mapped[str | None]
    active: Mapped[bool] = mapped_column(default=True)

    orders: Mapped[list["Order"]] = relationship(back_populates="user")
