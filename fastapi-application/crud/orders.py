from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import Order, User, Book
from core.schemas.order import OrderCreate


async def create_order(
    session: AsyncSession,
    order_create: OrderCreate,
) -> Order:
    order = Order(**order_create.model_dump())
    session.add(order)
    await session.commit()
    # await session.refresh(user)
    return order


async def get_order(session: AsyncSession, order_id: int):
    return await session.get(Order, order_id)


async def get_order_with_user(session: AsyncSession):
    stmt = select(Order).options(
        joinedload(Order.user),
    ).order_by(Order.id)
    orders = await session.scalars(stmt)
    return orders.all()


async def get_users_with_orders(session: AsyncSession):
    stmt = select(User).options(
        # joinedload(User.orders),
        selectinload(User.orders),
    ).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    return users.all()


async def get_user_with_orders(user_id: int, session: AsyncSession,):
    stmt = select(User).options(
        # joinedload(User.orders),
        selectinload(User.orders),
    ).where(User.id == user_id)
    user: User | None = await session.scalar(stmt)
    return user


async def add_book_in_order(session: AsyncSession, order_id: int, book_id: int):
    order = await session.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.books))
    )
    book = await session.get(Book, book_id)
    try:
        order.books.append(book)
        print("+++")
    finally:
        print("===")
        await session.commit()


async def get_orders_with_books(session: AsyncSession):
    stmt = (
        select(Order)
        .options(
            selectinload(Order.books)
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return orders.all()
