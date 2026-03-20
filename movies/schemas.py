from pydantic import BaseModel
from typing import List
from datetime import date


class GenreOut(BaseModel):
    """ GenreOut
    """
    id: int
    name: str


class MovieIn(BaseModel):
    """ MovieIn
    """
    title: str
    description: str
    release_date: date
    rating: float
    genre_ids: List[int] = []


class MovieOut(BaseModel):
    """ MovieOut
    """
    id: int
    title: str
    description: str
    release_date: date
    rating: float
    genres: List[GenreOut]


class ReviewIn(BaseModel):
    """ ReviewIn
    """
    movie_id: int
    text: str
    rating: int


class ReviewOut(BaseModel):
    """ ReviewOut
    """
    id: int
    user: str
    text: str
    rating: int
    created_at: str
