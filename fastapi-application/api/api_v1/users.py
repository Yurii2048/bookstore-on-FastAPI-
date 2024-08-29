from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import UserRead, UserCreate
from crud import users as users_crud

router = APIRouter(tags=["Users"])


@router.get("", response_model=list[UserRead])
async def get_users(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    users = await users_crud.get_all_users(session=session)
    return users


@router.get("/userID/{user_id}", response_model=UserRead)
async def get_user(
    username: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await users_crud.get_user_with_id(session=session, user_id=username)
    return user


@router.get("/username/{username}", response_model=UserRead)
async def get_user(
    username: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    user = await users_crud.get_user_by_username(session=session, username=username)
    return user


@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    user_create: UserCreate,
):
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )
    return user
