from src.db import engine
from sqlmodel import SQLModel


async def create_connection() -> None:
    async with engine.begin() as conn:
        from src.db.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)
