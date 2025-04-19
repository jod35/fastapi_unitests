from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from src import app
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
import pytest

from src.db.dependencies import get_session

DB_URL = Config.TEST_DATABASE_URL

test_engine = create_async_engine(
    url=DB_URL,
    echo=True
)

#create a session to override the default db session
async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)
    try:
        async with Session(bind=test_engine) as session:
            yield session
    finally:
        await session.close()

@pytest_asyncio.fixture(scope="session")
async def test_client():
    async with test_engine.begin() as conn:
        from src.db.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)

    # override the session
    app.dependency_overrides[get_session] = test_get_session
    
    with TestClient(app) as client:
        yield client 
    
@pytest_asyncio.fixture()
def test_book_payload():
    return {
        "title": "Python Testing with pytest",
        "author": "Brian Okken",
        "description": "A practical guide to using pytest for testing Python applications, including unit tests applicable to FastAPI.",
        "level": "Beginner to Intermediate",
        "date_published": "2017-09-25",
        "status": "PRIVATE"
    }

@pytest_asyncio.fixture()
def test_book_update_payload():
    return {
        "title": "Updated Python Testing with pytest",
        "author": "Brian Okken",
        "description": "An updated practical guide to using pytest for testing Python applications, including unit tests applicable to FastAPI.",
        "level": "Intermediate",
        "date_published": "2023-01-01",
        "status": "PUBLIC"
    }