from pydantic import BaseModel
from pydantic import ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    prise: int


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
