from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Order(IntIdPkMixin, Base):

    order_status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # books_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # price: Mapped[int] = mapped_column(Integer)
