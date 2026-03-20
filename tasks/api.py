from typing import List
from ninja import Router
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
from .models import Task
from .schemas import TaskIn, TaskOut
from .auth import SimpleBearerAuth

auth_scheme = SimpleBearerAuth()
router = Router()
ALLOWED_ORDER_FIELDS = ["created_at", "-created_at", "due_date", "-due_date"]


@router.post("/", response=TaskOut, auth=auth_scheme)
def create_task(request, data: TaskIn) -> Task:
    """Create a new task for the authenticated user
    """
    task = Task.objects.create(**data.dict(), owner=request.auth)
    return task


@router.get("/", response=List[TaskOut], auth=auth_scheme)
@paginate
def list_tasks(request, status: str = None, search: str = None, order_by: str = "-created_at"):
    """List all tasks
    """
    tasks = Task.objects.filter(owner=request.auth)

    if status:
        tasks = tasks.filter(status=status)

    if search:
        tasks = tasks.filter(title__icontains=search)

    if order_by not in ALLOWED_ORDER_FIELDS:
        order_by = "-created_at"

    return tasks.order_by(order_by)


@router.get("/{task_id}/", response=TaskOut, auth=auth_scheme)
def get_task(request, task_id: int) -> Task:
    """Get task by id
    """
    task = get_object_or_404(Task, id=task_id, owner=request.auth)
    return task


@router.put("/{task_id}/", response=TaskOut, auth=auth_scheme)
def update_task(request, task_id: int, data: TaskIn) -> Task:
    """Update task by id
    """
    task = get_object_or_404(Task, id=task_id, owner=request.auth)

    for attr, value in data.dict().items():
        setattr(task, attr, value)

    task.save()
    return task


@router.delete("/{task_id}/", auth=auth_scheme)
def delete_task(request, task_id: int) -> dict:
    """Delete task by id
    """
    task = get_object_or_404(Task, id=task_id, owner=request.auth)
    task.delete()
    return {"success": True}
