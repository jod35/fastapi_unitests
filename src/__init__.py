from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager

from src.db.connect import create_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_connection()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(book_router, prefix="/books")
