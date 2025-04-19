import uuid
from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: str = Field(
        primary_key=True, unique=True, default_factory=lambda: str(uuid.uuid4())
    )
    title: str
    author: str
    description: str
    level: str
    date_published: str
    status: str = Field(default="PUBLIC")

    def __repr__(self):
        return f"<Book {self.title}>"
