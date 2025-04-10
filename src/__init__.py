from fastapi import FastAPI
from src.books import book_router

app = FastAPI()

app.include_router(book_router, prefix='/books')