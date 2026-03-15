from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$")
    published_year: Optional[int] = Field(None, ge=1000, le=2100)
    genre: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$")
    published_year: Optional[int] = Field(None, ge=1000, le=2100)
    genre: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)


class Book(BookBase):
    id: str
    created_at: str
    updated_at: str


class BookListResponse(BaseModel):
    items: list[Book]
    count: int
    last_evaluated_key: Optional[str] = None
