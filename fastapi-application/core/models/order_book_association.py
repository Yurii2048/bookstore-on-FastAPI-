from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class OrderBookAssociation(IntIdPkMixin, Base):
    __tablename__ = "order_book_association"
    __table_args__ = (UniqueConstraint("order_id", "book_id"),)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))


# order_book_association_table = Table(
#     "order_book_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey("orders.id"), nullable=False),
#     Column("book_id", ForeignKey("books.id"), nullable=False),
#     UniqueConstraint("order_id", "book_id")
# )
