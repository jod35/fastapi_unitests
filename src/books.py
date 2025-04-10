from typing import List
import uuid
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from src.data import books
from src.schemas import BookSchema, BookCreateSchema, StatusEnum

book_router = APIRouter()

def get_book_by_id(book_id: str):
    for book in books:
        if book['id'] == book_id:
            return book
    return None

@book_router.get('/', response_model=List[BookSchema])
async def get_books(status: StatusEnum = None) ->List[BookSchema]:
    return [book for book in books if book["status"] == status.value] if status else books

@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(post:BookCreateSchema)-> dict:
    new_book = post.model_dump()
    new_book['id'] = str(uuid.uuid4())
    books.append(new_book)
    return new_book

@book_router.get('/{book_uid}',response_model=BookSchema)
async def get_book(book_uid:str) -> dict:
    book = get_book_by_id(book_uid)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not found")

@book_router.put('/{book_uid}',response_model=BookSchema)
async def update_book(book_uid:str, update_data: BookCreateSchema) -> dict:
    book = get_book_by_id(book_uid)
    update_dict = update_data.model_dump()
    if book:
        for k,v in update_dict.items():
            book[k] = v
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not found")


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid:str):
    book = get_book_by_id(book_uid)
    if book:
        books.remove(book)
        pass
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not found")