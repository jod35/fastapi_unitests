from typing import List
from fastapi import APIRouter, status, Depends
from src.books.schemas import BookSchema, BookCreateSchema, StatusEnum
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.crud import BookCRUD
from src.db.dependencies import get_session
from src.db.models import Book

book_router = APIRouter()
book_crud = BookCRUD()


@book_router.get("/", response_model=List[Book])
async def get_books(
    session: AsyncSession = Depends(get_session),
    status: StatusEnum = None,
) -> List[Book]:
    books = await book_crud.get_all_books(session, status)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_post(
    post: BookCreateSchema, session: AsyncSession = Depends(get_session)
) -> dict:
    new_book_dict = post.model_dump()
    new_book = await book_crud.create_book(session, new_book_dict)
    return new_book


@book_router.get("/{book_uid}", response_model=BookSchema)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_crud.get_book_by_uid(session, book_uid)
    return book


@book_router.put("/{book_uid}", response_model=BookSchema)
async def update_book(
    book_uid: str,
    update_data: BookCreateSchema,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_book = await book_crud.update_book(
        session, book_uid, update_data.model_dump()
    )
    return updated_book


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    await book_crud.delete_book(session, book_uid)
