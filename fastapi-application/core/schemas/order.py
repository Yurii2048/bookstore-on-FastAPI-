from typing import List

from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class OrderBase(BaseModel):
    order_status: str
    user_id: int
    date_create: datetime
    description: str | None


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


class User(BaseModel):
    id: int
    username: str


class OrderView(OrderRead):
    user: User


class UserByOrders(User):
    orders: List[OrderRead]
