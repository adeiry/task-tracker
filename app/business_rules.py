"""
Business rules for task status transitions.

Validates that status changes follow the allowed workflow.
"""

from datetime import date

from fastapi import HTTPException, status
from app.models import TaskResponse, TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """
    Validate that a status transition is allowed.

    Raises HTTPException with 422 Unprocessable Entity if the transition is invalid.
    """
    allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})

    if current == new:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )

    if (current, new) not in VALID_TRANSITIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )


def is_task_overdue(task: TaskResponse, today: date) -> bool:
    """
    A task is overdue when it has a due date earlier than today and is not Done.
    """
    return (
        task.due_date is not None
        and task.due_date < today
        and task.status != TaskStatus.DONE
    )
