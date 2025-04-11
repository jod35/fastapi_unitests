from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound
from src.db.models import Book
from enum import Enum


class BookStatus(Enum):
    PUBLISHED = "published"
    DRAFT = "draft"


class BookCRUD:
    """
    All methods expect an active AsyncSession with a transaction.
    The caller is responsible for committing or rolling back the session.
    """

    async def get_all_books(
        self,
        session: AsyncSession,
        status: Optional[str] = None,
    ) -> List[Book]:
        statement = select(Book).order_by(desc(Book.date_published))
        if status is not None:
            statement = statement.where(Book.status == status.value)

        result = await session.exec(statement)
        return result.all()

    async def get_book_by_uid(self, session: AsyncSession, book_uid: str):
        try:
            statement = select(Book).where(Book.id == book_uid)
            result = await session.exec(statement)
            book = result.one_or_none()
            return book
        except NoResultFound:
            raise HTTPException(f"Book with uuid {book_uid} not found.")

    async def create_book(self, session: AsyncSession, book_data: dict):
        book = Book(**book_data)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def update_book(
        self, session: AsyncSession, book_uid: str, book_update_data: dict
    ):
        book_to_update = await self.get_book_by_uid(session, book_uid=book_uid)

        for k, v in book_update_data.items():
            setattr(book_to_update, k, v)

        await session.commit()
        await session.refresh(book_to_update)

        return book_to_update

    async def delete_book(self, session: AsyncSession, book_uid: str):
        book_to_delete = await self.get_book_by_uid(session, book_uid=book_uid)
        await session.delete(book_to_delete)
        await session.commit()
