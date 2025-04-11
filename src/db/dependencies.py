from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db import engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)

    async with Session(bind=engine) as session:
        yield session
