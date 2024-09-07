from typing import Annotated

from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.demo_auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth import utils as auth_utils
from core.models import db_helper, User
from core.schemas.user import UserSchema
from crud.users import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
        )
    return payload


async def get_current_auth_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: dict = Depends(get_current_token_payload)
) -> UserSchema:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {token_type!r} expected {ACCESS_TOKEN_TYPE!r}",
        )
    username: str | None = payload.get("sub")
    if user := await get_user_by_username(session=session, username=username):
        return user
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )


async def get_current_auth_user_for_refresh(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: dict = Depends(get_current_token_payload)
) -> UserSchema:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    print(token_type)
    if token_type != REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type {token_type!r} expected {REFRESH_TOKEN_TYPE!r}",
        )
    username: str | None = payload.get("sub")
    if user := await get_user_by_username(session=session, username=username):
        return user
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )


async def validate_auth_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        username: str = Form(),
        password: str = Form(),

):
    unauthed_ext = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user: User = await get_user_by_username(session=session, username=username)
    if not user:
        raise unauthed_ext
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password
    ):
        raise unauthed_ext
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user
