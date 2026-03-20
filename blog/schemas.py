from pydantic import BaseModel
from typing import List
from datetime import datetime


class TagOut(BaseModel):
    id: int
    name: str


class PostIn(BaseModel):
    title: str
    content: str
    tag_ids: List[int] = []


class PostOut(BaseModel):
    id: int
    author: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagOut]


class CommentIn(BaseModel):
    post_id: int
    text: str


class CommentOut(BaseModel):
    id: int
    user: str
    text: str
    created_at: datetime
