from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
