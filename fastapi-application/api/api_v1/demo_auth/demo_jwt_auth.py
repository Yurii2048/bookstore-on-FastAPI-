from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.demo_auth.helpers import create_access_token, create_refresh_token
from api.api_v1.demo_auth.validation import (
    get_current_token_payload,
    get_current_auth_user_for_refresh,
    get_current_active_auth_user, validate_auth_user
)
from core.models import db_helper
from core.schemas.user import UserSchema, UserCreate, UserRead
from crud import users as users_crud

http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])


@router.post("/signup", response_model=UserRead)
async def auth_user_registration(
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


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(
        user: UserSchema = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/users/me")
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user)
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
