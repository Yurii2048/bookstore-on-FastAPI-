from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user import Order


class Book(IntIdPkMixin, Base):

    title: Mapped[str]
    author: Mapped[str]
    prise: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(
        secondary="order_book_association",
        back_populates="books",
    )
