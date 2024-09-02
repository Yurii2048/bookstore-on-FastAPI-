from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
# from .order_book_association import order_book_association_table
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user import User
    from .book import Book


class Order(IntIdPkMixin, Base):

    order_status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # books_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    date_create: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=func.now(),
    )
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # price: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship(back_populates="orders")
    books: Mapped[list["Book"]] = relationship(
        # secondary=order_book_association_table,
        secondary="order_book_association",
        back_populates="orders",
    )
