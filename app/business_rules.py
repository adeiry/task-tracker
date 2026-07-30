"""
Business rules for task status transitions.

Validates that status changes follow the allowed workflow.
"""

from datetime import date

from fastapi import HTTPException, status
from app.models import TaskResponse, TaskStatus, normalize_tag

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Validate that a status transition is allowed.

    Args:
        current (TaskStatus): The task's current status.
        new (TaskStatus): The requested new status.

    Returns:
        None: Returns nothing if the transition is allowed.

    Raises:
        HTTPException: 422 if ``current == new`` (a same-status
            "transition" is always rejected, not treated as a no-op), or
            if ``(current, new)`` is not one of the pairs in
            ``VALID_TRANSITIONS`` (``ToDo``→``InProgress``,
            ``InProgress``→``Done``, ``Done``→``InProgress``). The
            response body is ``{"detail": "<string>"}`` — a plain
            string, not the list-of-objects shape FastAPI's OpenAPI
            schema declares for automatic (Pydantic) 422 validation
            errors on this same route.

    Example:
        validate_status_transition(TaskStatus.TODO, TaskStatus.IN_PROGRESS)
        # Returns None; the transition is allowed.
    """
    allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})

    if current == new or (current, new) not in VALID_TRANSITIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )


def is_task_overdue(task: TaskResponse, today: date) -> bool:
    """Determine whether a task counts as overdue.

    A task is overdue when it has a due date, that due date is strictly
    earlier than ``today``, and its status is not ``Done``.

    Args:
        task (TaskResponse): The task to evaluate.
        today (date): The reference date to compare ``task.due_date``
            against. Callers (e.g. ``storage.get_all_tasks``) typically
            pass ``date.today()``.

    Returns:
        bool: ``True`` if the task is overdue, ``False`` otherwise
        (including when ``task.due_date`` is ``None``, when it equals
        ``today``, or when ``task.status`` is ``Done``).
    """
    return (
        task.due_date is not None
        and task.due_date < today
        and task.status != TaskStatus.DONE
    )


def task_has_tag(task: TaskResponse, tag: str) -> bool:
    """Check whether a task has a tag matching the given query.

    Matching is case-insensitive and ignores leading/trailing whitespace
    on both sides, and requires an exact match after normalization (no
    substring matching).

    Args:
        task (TaskResponse): The task to check.
        tag (str): The query tag to match against ``task.tags``.

    Returns:
        bool: ``True`` if any of ``task.tags`` matches ``tag`` after
        normalization, ``False`` otherwise (including when ``task.tags``
        is empty).
    """
    query = normalize_tag(tag)
    return any(normalize_tag(existing) == query for existing in task.tags)
