# AI Prompt Log

This document records the main AI interactions used during the mid-course project.

## Prompt 1 — Project Planning

### Goal

Select two features that provide meaningful backend, frontend, testing, and documentation work without adding unnecessary architecture.

### Prompt

Recommend two features for extending an existing FastAPI and vanilla JavaScript Task Tracker.

Current functionality:

- Create, list, edit, and delete tasks
- Status transitions
- Priority and status filtering
- Kanban board
- Drag and drop
- Modal create and edit form
- In-memory storage
- Pytest API tests

Constraints:

- Keep the existing architecture.
- Do not add authentication, a production database, real-time updates, or deployment.
- The features must be visible in the frontend.
- The features must be testable with pytest.
- Prefer the smallest meaningful scope.

Compare due dates, tags, comments, and activity history. Recommend two features but explain the tradeoffs.

### Decision

Selected due dates and tags because they offer visible user value while requiring fewer structural changes than comments or activity history.

## Prompt 2 — User Stories and Architecture

### Goal

Define the feature behavior before implementation.

### Prompt

Write user stories, acceptance criteria, validation rules, and a small architecture decision record for adding:

1. Optional due dates with overdue identification and filtering.
2. Tags with normalization, duplicate prevention, display, and filtering.

Preserve the existing FastAPI, Pydantic, in-memory storage, pytest, and vanilla JavaScript architecture.

### Result Used

The resulting user stories and architecture decisions were reviewed and recorded in:

- `docs/user-stories.md`
- `docs/mini-adr.md`