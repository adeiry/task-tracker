from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def normalize_tag(value: str) -> str:
    """Normalize a tag value for case-insensitive comparison.

    Args:
        value (str): The raw tag value.

    Returns:
        str: ``value`` with surrounding whitespace removed and converted
        to lowercase. Used as the comparison key for deduplication
        (``_normalize_tags``) and for tag filtering/matching
        (``business_rules.task_has_tag``); it is not the value stored on
        the task, which preserves the original casing.
    """
    return value.strip().lower()


def _normalize_tags(tags: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        cleaned = tag.strip()
        if not cleaned:
            raise ValueError("tags cannot be blank")
        key = normalize_tag(tag)
        if key in seen:
            continue
        seen.add(key)
        normalized.append(cleaned)
    return normalized


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: date | None = None
    tags: list[str] = []

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate and normalize a task title.

        Args:
            v (str): The raw title value.

        Returns:
            str: ``v`` with surrounding whitespace removed.

        Raises:
            ValueError: If ``v`` is blank after trimming, or longer than
                200 characters. Pydantic converts this into an HTTP 422
                response at the API layer.
        """
        v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        if len(v) > 200:
            raise ValueError("title must be at most 200 characters")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Validate and normalize a task's tag list.

        Delegates to ``_normalize_tags``: trims whitespace, rejects blank
        entries, and removes case-insensitive duplicates (keeping the
        first occurrence's casing).

        Args:
            v (list[str]): The raw tag values.

        Returns:
            list[str]: The trimmed, deduplicated tag list.

        Raises:
            ValueError: If any tag is blank or whitespace-only after
                trimming. Pydantic converts this into an HTTP 422 response
                at the API layer.
        """
        return _normalize_tags(v)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: date | None = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize a task title for partial updates.

        Args:
            v (str | None): The raw title value, or ``None`` if ``title``
                was not included in the update.

        Returns:
            str | None: ``None`` unchanged if the field was not provided;
            otherwise ``v`` with surrounding whitespace removed.

        Raises:
            ValueError: If ``v`` is provided but blank after trimming, or
                longer than 200 characters. Pydantic converts this into an
                HTTP 422 response at the API layer.
        """
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        if len(v) > 200:
            raise ValueError("title must be at most 200 characters")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Validate and normalize a tag list for partial updates.

        Args:
            v (list[str] | None): The raw tag values, or ``None`` if
                ``tags`` was not included in the update.

        Returns:
            list[str] | None: ``None`` unchanged if the field was not
            provided; otherwise the trimmed, deduplicated tag list (see
            ``_normalize_tags``).

        Raises:
            ValueError: If any tag is blank or whitespace-only after
                trimming. Pydantic converts this into an HTTP 422 response
                at the API layer.
        """
        if v is None:
            return v
        return _normalize_tags(v)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: date | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime
