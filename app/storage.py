import uuid
from datetime import date, datetime, timezone
from typing import Optional

from app.business_rules import is_task_overdue, task_has_tag
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and persist a new task from already-validated input.

    Args:
        payload (TaskCreate): The validated task data.

    Returns:
        TaskResponse: The stored task, with a generated ``id`` (UUID4)
        and ``created_at``/``updated_at`` set to the current UTC time.
        ``description`` is stored as ``""`` if ``payload.description``
        is falsy (``None`` or empty).
    """
    now = datetime.now(timezone.utc)
    task_id = str(uuid.uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        tags=payload.tags,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    """Return stored tasks, optionally narrowed by one or more filters.

    Each provided filter is applied in sequence (status, then priority,
    then overdue, then tag), so combining filters produces an AND of all
    conditions. Filters left as ``None`` are skipped entirely.

    Args:
        status (TaskStatus | None): Exact status to match, or ``None`` to
            skip this filter.
        priority (TaskPriority | None): Exact priority to match, or
            ``None`` to skip this filter.
        overdue (bool | None): If not ``None``, keep only tasks where
            ``is_task_overdue(task, date.today()) == overdue``.
        tag (str | None): If not ``None``, keep only tasks where
            ``task_has_tag(task, tag)`` is ``True``.

    Returns:
        list[TaskResponse]: The tasks matching every provided filter.
        [VERIFY: order reflects dict insertion order in ``_tasks``, not
        an explicit sort — not documented as an intentional contract.]
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if overdue is not None:
        today = date.today()
        tasks = [task for task in tasks if is_task_overdue(task, today) == overdue]
    if tag is not None:
        tasks = [task for task in tasks if task_has_tag(task, tag)]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a single task by id.

    Args:
        task_id (str): The task's unique identifier.

    Returns:
        Optional[TaskResponse]: The matching task, or ``None`` if no task
        with ``task_id`` exists.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to a stored task.

    Only fields explicitly set on ``payload`` (via
    ``model_dump(exclude_unset=True)``) overwrite the stored values; an
    explicitly-sent ``null`` counts as set. ``updated_at`` is refreshed to
    the current UTC time whenever at least one field is updated.

    Args:
        task_id (str): The task's unique identifier.
        payload (TaskUpdate): The fields to update.

    Returns:
        Optional[TaskResponse]: ``None`` if no task with ``task_id``
        exists. If ``payload`` has no explicitly-set fields, the existing
        task is returned unchanged (``updated_at`` is not refreshed in
        that case). Otherwise, the updated task.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    task_data = task.model_dump()
    task_data.update(updates)
    task_data["updated_at"] = datetime.now(timezone.utc)

    updated_task = TaskResponse(**task_data)
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    """Remove a stored task by id.

    Args:
        task_id (str): The task's unique identifier.

    Returns:
        bool: ``True`` if a task was found and removed, ``False`` if no
        task with ``task_id`` existed.
    """
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()
