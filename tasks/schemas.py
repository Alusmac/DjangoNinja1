from ninja import Schema
from datetime import datetime
from typing import Optional


class TaskIn(Schema):
    """Schema for creating a task
    """
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskOut(Schema):
    """Schema for returning task data
    """
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    due_date: Optional[datetime]


class TaskUpdate(Schema):
    """Schema for updating a task
    """
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    due_date: Optional[datetime]
