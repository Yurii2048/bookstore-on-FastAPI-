from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.order import OrderCreate, OrderRead, OrderView, UserByOrders
from crud import orders as orders_crud

router = APIRouter(tags=["Order"])


@router.get("", response_model=list[UserByOrders])
async def get_orders(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    result = await orders_crud.get_users_with_orders(session=session)
    return result


@router.get("/all_orders", response_model=list[OrderView])
async def get_all_orders(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    result = await orders_crud.get_order_with_user(session=session)
    return list(result)


@router.get("/order/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    order = await orders_crud.get_order(
        session=session,
        order_id=order_id,
    )
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return order


@router.post("", response_model=OrderRead)
async def create_order(
    order_create: OrderCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    order = await orders_crud.create_order(
        session=session,
        order_create=order_create
    )
    return order


@router.get("/user/{user_id}", response_model=UserByOrders)
async def get_user_with_orders(
    user_id: int,
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    result = await orders_crud.get_user_with_orders(user_id=user_id, session=session)
    print(result)
    if result is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return result


@router.post("/manipulations")
async def add_to_order(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_id: int,
    book_id: int,
):
    await orders_crud.add_book_in_order(session=session, order_id=order_id, book_id=book_id)
    return {"message": "success"}


@router.get("/all_all")
async def get_all_orders_book(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    result = await orders_crud.get_orders_with_books(session=session)
    return result
