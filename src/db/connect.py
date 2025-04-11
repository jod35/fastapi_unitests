from src.db import engine
from sqlmodel import SQLModel


async def create_connection() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
