from pydantic import BaseModel
from datetime import datetime, date
from typing import List


class GenreOut(BaseModel):
    """GenreOut
    """
    id: int
    name: str


class BookIn(BaseModel):
    """Book information
    """
    title: str
    author: str
    description: str = ""
    published_date: date
    genre_ids: List[int] = []


class BookOut(BaseModel):
    """Book out
    """
    id: int
    title: str
    author: str
    description: str
    published_date: date
    genres: List[GenreOut]


class RentalIn(BaseModel):
    """RentalIn
    """
    book_id: int
    due_date: datetime


class RentalOut(BaseModel):
    """Rental
    """
    id: int
    book_id: int
    book_title: str
    user: str
    rented_at: datetime
    due_date: datetime
    returned: bool
