# Mini Architecture Decision Record

## Title

Add Due Dates and Tags to the Task Tracker

## Status

Accepted

## Context

The Task Tracker already supports task creation, editing, deletion, status transitions, priority, assignee, filtering, and a Kanban board.

The mid-course project requires two meaningful features that extend both the backend and frontend while remaining small enough to implement, test, verify, and document within the project scope.

The selected features are:

1. Optional due dates with overdue identification and filtering.
2. Tags with task-card display and tag filtering.

## Decision

Extend the existing task model instead of creating separate database entities or services.

The task model will include:

- An optional `due_date` field.
- A `tags` field containing a list of strings.

The existing task create, response, and update models will be extended to support these fields.

The existing in-memory storage structure will continue to be used.

The frontend modal and task cards will be updated to support both fields.

Filtering will remain a frontend responsibility because the current application already loads the task list and displays it on the Kanban board.

## Due-Date Rules

- The due date is optional.
- The API will accept a date value in ISO format: `YYYY-MM-DD`.
- A task is overdue when:
  - it has a due date,
  - the due date is before the current date,
  - and the task status is not `Done`.
- Overdue status will be calculated rather than permanently stored.

## Tag Rules

- A task can contain zero or more tags.
- Tags will be stored as a list of strings.
- Leading and trailing spaces will be removed.
- Empty tags will be rejected or removed.
- Duplicate tags will not be stored more than once.
- Tag comparison will be case-insensitive for duplicate detection and filtering.

## Alternatives Considered

### Separate tag entity

A separate tag model and endpoint could support reusable tag management.

This was rejected because it would introduce additional routes, relationships, and storage complexity that are unnecessary for the current learning project.

### Separate activity or comments feature

Comments or activity history could provide more advanced collaboration.

These were rejected because they require separate records, identifiers, timestamps, additional endpoints, and significantly more frontend behavior.

### Store an `is_overdue` field

The application could store whether each task is overdue.

This was rejected because overdue status changes with time and can be calculated from the due date and task status.

## Consequences

### Positive

- Both features are visible in the user interface.
- Both features require meaningful backend and frontend work.
- The existing architecture remains simple.
- The features can be tested with pytest.
- No new database or external dependency is required.

### Negative

- Tags are stored directly inside each task and are not centrally managed.
- Frontend filtering may become more complex as more filters are added.
- Overdue calculations depend on the current date and require careful testing.