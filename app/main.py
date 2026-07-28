"""
Task Tracker API - Application Entry Point

This module creates the FastAPI application instance.
CRUD endpoints will be added in a future iteration; this
skeleton currently exposes only a health check endpoint.
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

app = FastAPI(
    title="Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Report service liveness.

    Returns:
        dict: A payload with ``status`` (always ``"ok"``) and
        ``timestamp`` (current UTC time in ISO 8601 format).

    Example:
        GET /health

        Response (200): {"status": "ok", "timestamp": "2026-01-01T00:00:00+00:00"}
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
    tag: str | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status, priority, overdue state, and tag.

    Every provided filter is combined with AND logic; filters left as
    ``None`` are skipped entirely.

    Args:
        status (TaskStatus | None): Exact status to match, or ``None`` to
            skip this filter.
        priority (TaskPriority | None): Exact priority to match, or
            ``None`` to skip this filter.
        overdue (bool | None): When ``True``, only overdue tasks are
            returned; when ``False``, only non-overdue tasks are returned
            (the logical complement of ``True``); when omitted (``None``),
            no overdue filtering is applied. See
            ``business_rules.is_task_overdue`` for the overdue rule.
        tag (str | None): When provided, only tasks with a tag equal to
            this value after case-insensitive, whitespace-trimmed
            normalization are returned. See ``business_rules.task_has_tag``.

    Returns:
        list[TaskResponse]: The tasks matching every provided filter.
        [VERIFY: return order reflects dict insertion order in
        ``storage._tasks``, not an explicit sort — this is not documented
        anywhere as an intentional ordering contract.]

    Raises:
        HTTPException: Not raised directly by this function; FastAPI
            returns HTTP 422 automatically if ``status``/``priority`` is
            not a valid enum value, or ``overdue`` cannot be parsed as a
            boolean.

    Example:
        GET /tasks?status=ToDo&priority=High&overdue=true&tag=urgent
    """
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue, tag=tag)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload (TaskCreate): The task to create. Already validated by
            Pydantic before this function runs: ``title`` must be
            non-blank and at most 200 characters; ``tags`` are trimmed and
            case-insensitively deduplicated, and rejected if any entry is
            blank after trimming; unknown fields are rejected
            (``extra="forbid"``).

    Returns:
        TaskResponse: The newly created task, including a generated
        ``id`` and ``created_at``/``updated_at`` timestamps.

    Raises:
        HTTPException: Not raised directly by this function; FastAPI
            returns HTTP 422 automatically if ``payload`` fails model
            validation.

    Example:
        POST /tasks
        Body: {"title": "Write tests", "priority": "High"}
    """
    return storage.add_task(payload)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by id.

    Args:
        task_id (str): The task's unique identifier.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        GET /tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task.

    Only fields explicitly present in ``payload`` are changed; omitted
    fields keep their current stored value (``storage.update_task`` uses
    ``exclude_unset=True``). An explicitly-sent ``null`` (e.g.
    ``"due_date": null``) counts as set and overwrites the existing value.

    If ``payload.status`` is omitted, the status is left unchanged and no
    transition validation is performed. If ``payload.status`` is
    provided, the transition from the task's current status to the new
    status is validated via ``business_rules.validate_status_transition``
    before the update is applied.

    Args:
        task_id (str): The task's unique identifier.
        payload (TaskUpdate): The fields to update.

    Returns:
        TaskResponse: The task after the update is applied.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.
        HTTPException: 422 if ``payload.status`` is provided and the
            transition from the current status is not allowed, including
            a same-status "transition".

    Example:
        PATCH /tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6
        Body: {"status": "InProgress"}
    """
    if payload.status is None:
        task = storage.update_task(task_id, payload)
        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        return task

    existing_task = storage.get_task_by_id(task_id)
    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    validate_status_transition(existing_task.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by id.

    Args:
        task_id (str): The task's unique identifier.

    Returns:
        None: On success, no response body is returned (HTTP 204).

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        DELETE /tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6
    """
    if not storage.delete_task(task_id):
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )