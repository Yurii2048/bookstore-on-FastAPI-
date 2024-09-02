from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.book import BookCreate, BookRead
from crud import books as books_crud

router = APIRouter(tags=["Books"])


@router.get("", response_model=list[BookRead])
async def get_books(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    books = await books_crud.get_all_books(session=session)
    return books


@router.get("/bookID/{book_id}", response_model=BookRead)
async def get_book(
    book_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    book = await books_crud.get_book(session=session, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    return book


@router.post("", response_model=BookRead)
async def create_book(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    book_create: BookCreate,
):
    book = await books_crud.create_book(
        session=session,
        book_create=book_create,
    )
    return book


@router.delete("/delete/{book_id}")
async def delete_book(
    book_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    await books_crud.remove_book(book_id=book_id, session=session)
    return {"message": f"delete {book_id} - success"}
