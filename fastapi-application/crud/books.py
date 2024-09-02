from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Book
from core.schemas.book import BookCreate


async def create_book(
    session: AsyncSession,
    book_create: BookCreate,
) -> Book:
    book = Book(**book_create.model_dump())
    session.add(book)
    await session.commit()
    # await session.refresh(user)
    return book


async def get_all_books(
    session: AsyncSession,
) -> Sequence[Book]:
    stmt = select(Book).order_by(Book.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_book(session: AsyncSession, book_id: int):
    return await session.get(Book, book_id)


async def remove_book(session: AsyncSession, book_id):
    stmt = await session.get(Book, book_id)
    if stmt is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    else:
        await session.delete(stmt)
    await session.commit()
