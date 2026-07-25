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

## Prompt 3 – Backend Inspection

### Tool
Claude Code

### Goal
Understand the backend changes required before making any edits.

### Prompt
Inspect this Task Tracker backend before changing anything.

I want to add an optional due_date field to tasks.

Requirements:
- Use Python date values.
- The API JSON format must be YYYY-MM-DD.
- due_date must be optional.
- Existing requests without due_date must continue working.
- due_date must be supported when creating a task.
- due_date must be supported in task responses.
- due_date must be supported in partial PATCH updates.
- Invalid date formats must return FastAPI/Pydantic validation errors.
- Do not change the frontend yet.
- Do not add overdue logic yet.
- Do not edit files yet.

Inspect:
- app/models.py
- app/storage.py
- app/main.py
- tests/test_tasks.py

Explain exactly which files and models need changes and identify any backward-compatibility risks.

### Outcome
Claude identified the required changes to the Pydantic models, storage layer, and tests without suggesting unnecessary architectural changes.

## Prompt 4 – Due Date Implementation

### Tool
Claude Code

### Goal
Implement backend support for due dates.

### Prompt
Implement the optional due_date backend support now.

Constraints:
- Modify only the files required for due_date support.
- Use datetime.date, not datetime.datetime.
- TaskCreate should default due_date to None.
- TaskResponse should include due_date.
- TaskUpdate must allow the due date to be changed.
- Preserve all existing fields and behavior.
- Do not implement tags.
- Do not implement overdue calculations.
- Do not change the frontend.
- Do not refactor unrelated code.

After editing, show me a concise summary of every change.

### Outcome
Claude updated the task models and storage logic to support optional due dates while preserving backward compatibility.

## Prompt 5 – Due Date Backend Tests

### Tool
Claude Code

### Goal
Add automated tests to verify the new due date functionality without affecting the existing test suite.

### Prompt
Add focused pytest tests for the new due_date behavior.

Add tests covering:

1. Creating a task with a valid due_date returns 201 and returns the same ISO date.
2. Creating a task without due_date still works and returns due_date as null.
3. Creating a task with an invalid due_date returns 422.
4. Patching an existing task updates its due_date.
5. Patching due_date to null clears an existing due date.

Follow the existing test structure and fixtures in tests/test_tasks.py.
Do not weaken or modify existing tests.
Do not add frontend tests.
After editing, run the full pytest suite.

### Outcome
Claude added pytest tests covering valid due dates, missing due dates, invalid date validation, updating an existing due date, and clearing a due date with `null`. The tests followed the existing project structure and preserved the original test suite.

### Verification
Ran:

```bash
python -m pytest -v
```
---

## Prompt 6 – Frontend Inspection

### Tool
Claude Code

### Goal
Understand the existing frontend structure before implementing due date support and identify the minimum changes required.

### Prompt
Inspect the frontend before making any changes.

I have already implemented optional due_date support in the backend.

Inspect:

- frontend/index.html
- frontend/script.js (or equivalent)
- frontend/styles.css (or equivalent)

Explain:

- where the create/edit modal is implemented
- where task cards are rendered
- where filters are implemented
- the smallest changes required to support due dates

Do not edit any files.
Do not implement anything yet.
Do not suggest unrelated refactoring.

### Outcome
Claude identified the frontend files responsible for the task form, task card rendering, and filtering logic. It outlined the minimum changes required to add due date support while preserving the existing architecture.

### Verification
Reviewed Claude's recommendations and confirmed they aligned with the current project structure before making any changes.

---

## Prompt 7 – Frontend Due Date Implementation

### Tool
Claude Code

### Goal
Implement frontend support for creating, editing, and displaying task due dates while preserving existing functionality.

### Prompt
Implement due date support in the frontend.

Requirements:

- Add a Due Date field to the create task form.
- Add a Due Date field to the edit task form.
- Send due_date to the existing backend API.
- Display the due date on every task card when present.
- Do not display anything if no due date exists.
- Preserve all existing functionality.
- Do not implement tags.
- Do not implement overdue highlighting yet.
- Do not refactor unrelated code.

After editing, summarize every change.

### Outcome
Claude updated the frontend forms to support optional due dates, included the due_date value in API requests, and displayed the due date on task cards when available while preserving existing functionality.

### Verification
Manually verified that:
- Tasks can be created with or without a due date.
- Existing tasks continue to work.
- Due dates are displayed correctly.
- Editing a task updates the displayed due date.

---

## Prompt 8 – Overdue Highlighting

### Tool
Claude Code

### Goal
Provide a clear visual indication when a task becomes overdue.

### Prompt
Implement overdue highlighting.

Rules:

- A task is overdue when:
  - due_date exists
  - due_date is before today's date
  - status is not Done

Display a clear visual indicator.

Examples:

- red border
- badge
- red text

Keep the implementation simple.

Do not modify backend code.
Do not implement filtering yet.
Do not refactor unrelated code.

### Outcome
Claude implemented frontend logic to identify overdue tasks and added a visual indicator to overdue task cards without modifying the backend.

### Verification
Created tasks with past and future due dates and confirmed that:
- Past due tasks were highlighted.
- Future tasks were not highlighted.
- Tasks marked as Done were not highlighted even if their due date had passed.

---

## Prompt 9 – Overdue Filter

### Tool
Claude Code

### Goal
Allow users to filter the Kanban board to display only overdue tasks.

### Prompt
Add an Overdue filter to the frontend.

Requirements:

- Add an Overdue option to the existing filters.
- When enabled:
    show only overdue tasks.
- When disabled:
    restore the normal board.
- Preserve existing filtering behavior.
- Do not modify backend routes.

### Outcome
Claude added an overdue filter that integrates with the existing frontend filtering logic without requiring backend changes.

### Verification
Verified that:
- Enabling the filter displayed only overdue tasks.
- Disabling the filter restored the full task list.
- Existing board functionality continued to work correctly.

---

## Prompt 10 – Frontend Verification Review

### Tool
Claude Code

### Goal
Review the completed due date implementation before continuing with the next feature.

### Prompt
Verify the due date implementation without making any code changes.

Review both the backend and frontend and confirm that the implementation satisfies these requirements:

Backend:
- due_date is optional.
- Creating a task without due_date still works.
- Creating a task with a valid due_date works.
- Invalid due_date values return validation errors.
- due_date can be updated.
- due_date can be cleared by setting it to null.
- Existing functionality remains unchanged.

Frontend:
- The create task form includes a Due Date field.
- The edit task form includes a Due Date field.
- The due date is displayed on task cards when present.
- Tasks without a due date display correctly.
- Overdue tasks are visually highlighted.
- The Overdue filter correctly shows only overdue tasks.

Testing:
- Review the existing pytest suite and confirm it still covers the backend correctly.
- Identify any gaps in testing, but do not add new tests.
- Confirm whether the implementation appears complete based on the current code.

Do not edit any files.
Do not refactor any code.
Provide only:
1. A checklist of satisfied requirements.
2. Any missing or incorrect behavior.
3. Any recommendations before final submission.

### Outcome
Claude reviewed the completed implementation and confirmed that the due date feature was fully integrated across the backend and frontend. It also identified any minor improvements and verified that the implementation remained consistent with the existing project architecture.

### Verification
- Ran the complete pytest suite successfully.
- Manually verified task creation, editing, overdue highlighting, and overdue filtering.
- Confirmed that existing functionality continued to work without regression.