from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.user import UserCreate
from auth import utils as auth_utils


async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user_by_username(
        session: AsyncSession,
        username: str,
) -> User:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    print(user)
    return user


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    user.password = auth_utils.hash_password(user.password)
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def get_user_with_id(session: AsyncSession, user_id: int):
    return await session.get(User, user_id)
