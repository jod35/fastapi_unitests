from enum import Enum
from pydantic import BaseModel

class StatusEnum(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

class BookSchema(BaseModel):
    id: str
    title: str
    author: str
    description: str
    level: str
    date_published: str
    status: str

class BookCreateSchema(BaseModel):
    title: str
    author: str
    description: str
    level: str
    date_published: str
    status: str = "PUBLIC"