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

---

## Prompt 11 – Tags Feature Inspection

### Tool
Claude Code

### Goal
Understand the minimum backend and frontend changes required to add task tags while preserving the existing project architecture.

### Prompt
Inspect the current Task Tracker project before implementing tags.

The project already supports:

- CRUD
- Status transitions
- Due dates
- Overdue highlighting
- Overdue filtering

Inspect:

- app/models.py
- app/storage.py
- app/main.py
- tests/test_tasks.py
- frontend/index.html
- frontend/script.js (or equivalent)
- frontend/styles.css (or equivalent)

Explain:

- the minimum backend changes
- the minimum frontend changes
- where tags should be stored
- how tag filtering should integrate with the existing filters

Do not edit any files.
Do not implement anything yet.
Do not suggest unrelated refactoring.

### Outcome
Claude identified the backend models, storage layer, frontend forms, task card rendering, and filtering logic that needed to be updated. It recommended storing tags as a list of strings within each task while preserving the existing architecture.

### Verification
Reviewed the proposed implementation plan and confirmed it aligned with the project's architecture before making any code changes.

---

## Prompt 12 – Backend Tag Implementation

### Tool
Claude Code

### Goal
Implement backend support for task tags while preserving existing functionality.

### Prompt
Implement backend support for task tags.

Requirements:

- Add an optional tags field to tasks.
- Store tags as a list of strings.
- Default to an empty list.
- Support creating tasks with tags.
- Support updating tags.
- Return tags in API responses.

Validation:

- Remove leading/trailing whitespace.
- Ignore empty tags.
- Prevent duplicate tags.
- Duplicate detection should be case-insensitive.

Constraints:

- Preserve all existing behavior.
- Do not modify due date functionality.
- Do not implement frontend changes.
- Do not refactor unrelated code.

After editing, summarize every change.

### Outcome
Claude extended the backend task models and storage logic to support tags. Tag normalization, duplicate removal, and validation were implemented while maintaining backward compatibility with the existing API.

### Verification
Verified that:
- Existing API behavior remained unchanged.
- Tasks could be created and updated with tags.
- Normalization and validation behaved as expected.
- Existing backend tests continued to pass.

---

## Prompt 13 – Backend Tag Tests

### Tool
Claude Code

### Goal
Verify that the backend tag functionality behaves correctly using automated tests.

### Prompt
Add focused pytest tests for task tags.

Add tests covering:

1. Create task with multiple tags.
2. Create task without tags.
3. Empty tags are ignored.
4. Duplicate tags are removed.
5. Updating tags replaces the existing list.

Follow the existing test structure.

Do not modify existing tests.

Run the complete pytest suite after editing.

### Outcome
Claude added backend tests covering valid tag creation, optional tags, normalization, duplicate removal, and tag updates while preserving the existing test suite.

### Verification
- Ran the complete pytest suite successfully.
- Intentionally modified one assertion to create a failing test.
- Confirmed the failure.
- Restored the correct assertion.
- Re-ran the suite and confirmed all tests passed.

---

## Prompt 14 – Frontend Tag Implementation

### Tool
Claude Code

### Goal
Allow users to create, edit, and display task tags from the frontend.

### Prompt
Implement frontend support for task tags.

Requirements:

- Add a Tags input to the create task form.
- Add a Tags input to the edit task form.
- Accept comma-separated values.
- Convert the input into a list before sending it to the backend.
- Display tags on every task card.
- Preserve existing functionality.
- Do not modify due date functionality.
- Do not refactor unrelated code.

Summarize every change after editing.

### Outcome
Claude updated the task forms to support comma-separated tag input, converted user input into a list before sending it to the backend, and displayed task tags on each Kanban card.

### Verification
Manually verified that:
- Tasks can be created with tags.
- Existing tasks can be edited.
- Tags are displayed correctly.
- Tasks without tags continue to display normally.

---

## Prompt 15 – Tag Filtering

### Tool
Claude Code

### Goal
Allow users to filter the Kanban board by task tag.

### Prompt
Implement tag filtering.

Requirements:

- Add a Tag filter to the existing filters.
- Allow filtering by a single tag.
- Filtering should be case-insensitive.
- Preserve existing status, priority, and overdue filtering.
- Do not modify backend routes.

### Outcome
Claude integrated tag filtering into the existing frontend filtering system using case-insensitive comparisons while preserving the existing filtering behavior.

### Verification
Manually verified that:
- Selecting a tag displayed only matching tasks.
- Clearing the filter restored the complete task list.
- Status, priority, and overdue filters continued to work correctly alongside the new tag filter.

---

## Prompt 16 — Frontend Task Deletion

### Tool 
Claude Code

### Goal 
Expose the existing backend task deletion functionality in the frontend.

### Prompt

> Inspect the existing task deletion implementation before making changes.
>
> The FastAPI backend already has a DELETE task endpoint and existing pytest coverage.
>
> Inspect the frontend and determine whether users can currently delete tasks from the UI.
>
> If deletion is missing from the frontend, implement it with these requirements:
>
> - Add a clearly labeled Delete action to the edit modal or task card.
> - Ask for confirmation before deleting.
> - Call the existing DELETE endpoint.
> - Remove the task from the board after a successful response.
> - Show a clear error message if deletion fails.
> - Close the modal after successful deletion.
> - Preserve all existing create, edit, drag-and-drop, due-date, tag, and filter behavior.
>
> Constraints:
>
> - Do not modify backend deletion behavior unless a real defect is found.
> - Do not add new dependencies.
> - Do not refactor unrelated code.
> - Do not remove existing tests.
>
> After editing, summarize the changes and provide a manual verification checklist.

### Outcome

The frontend was updated to expose the existing task deletion functionality. A delete action, confirmation step, API integration, UI update, and failure handling were added.

### Verification

- Created and deleted a temporary task
- Confirmed the task disappeared from the board
- Confirmed other tasks were not affected
- Confirmed failed deletion requests display an error
- Reran the backend test suite

---

## Prompt 17 — Frontend Polish

### Tool 
Claude Code

### Goal 
Improve the frontend presentation without changing application behavior.

### Prompt

> Polish the existing Task Tracker frontend without changing application behavior.
>
> Goals:
>
> - Make the interface feel more modern and consistent.
> - Improve spacing, typography, button states, task cards, filters, tags, due dates, and overdue indicators.
> - Add subtle hover and modal animations.
> - Improve drag-and-drop visual feedback.
> - Keep the current layout and functionality.
> - Preserve accessibility and readable contrast.
>
> Constraints:
>
> - Do not change backend code.
> - Do not add a frontend framework or external animation library.
> - Do not change API requests.
> - Do not remove or rename existing elements used by JavaScript.
> - Do not refactor unrelated logic.
> - Keep animations subtle and fast.
> - Review the existing HTML, CSS, and JavaScript before editing.
>
> After editing, summarize the visual changes and confirm that no functionality was intentionally changed.

### Outcome

The frontend styling was improved while preserving the existing application behavior. Task cards, buttons, filters, forms, tags, due dates, states, and drag-and-drop feedback were refined.

### Verification

- Manually tested all core workflows
- Verified due-date and tag functionality
- Verified task deletion
- Verified loading, empty, populated, and error states
- Reran the complete backend test suite

---

## Prompt 18 — Fix Overdue Filtering

### Tool
Claude Code

### Goal

Correct the overdue filtering implementation based on the reported review issue while preserving the existing API behavior.

### Prompt

Review the overdue filtering implementation in the Task Tracker backend.

The current implementation does not correctly handle all overdue filtering scenarios.

Requirements:

- Identify the root cause.
- Fix only the overdue filtering logic.
- Preserve the existing API contract and response format.
- Do not modify tests to make the implementation pass.
- Do not introduce unrelated refactoring.
- After implementing the fix, rerun the affected tests and the complete pytest suite.
- Summarize the root cause, implemented fix, and verification results.

### Outcome

Claude identified the root cause of the overdue filtering issue, implemented a focused fix, and preserved the existing application behavior without introducing unrelated changes.

### Verification

- Reran the overdue filtering tests.
- Verified overdue filtering manually through the API and frontend.
- Reran the complete pytest suite successfully.

---

## Prompt 19 — Fix Tag Filtering

### Tool
Claude Code

### Goal

Correct the tag filtering implementation based on the reported review issue while preserving the existing filtering behavior.

### Prompt

Review the tag filtering implementation in the Task Tracker backend.

The current implementation does not satisfy the expected tag filtering behavior.

Requirements:

- Identify the root cause.
- Fix only the tag filtering implementation.
- Preserve existing API behavior.
- Do not weaken or modify existing tests.
- Preserve case-insensitive matching and whitespace normalization.
- Do not introduce unrelated refactoring.
- Rerun the affected tests followed by the complete pytest suite.
- Summarize the implemented fix and verification results.

### Outcome

Claude corrected the tag filtering implementation while preserving the existing API contract and filtering behavior.

### Verification

- Reran the tag filtering tests.
- Verified tag filtering manually through the API and frontend.
- Reran the complete pytest suite successfully.

---

## Prompt 20 — Business Rules Refactor

### Tool
Claude Code

### Goal

Improve the readability and maintainability of the business rules without changing application behavior.

### Prompt

Perform a small, behavior-preserving refactor of `app/business_rules.py`.

Requirements:

- Inspect the existing implementation and related tests.
- Select one small section that can be improved.
- Refactor only the selected section.
- Improve readability by simplifying logic, extracting a helper, improving naming, or removing duplication.
- Preserve all public behavior, validation rules, status transitions, and overdue calculation.
- Do not modify tests.
- Do not introduce new functionality.
- After the refactor, rerun the affected tests and the complete pytest suite.
- Summarize the selected refactor and explain why it preserves behavior.

### Outcome

Claude performed a focused refactor of the business rules, improving code readability and maintainability while preserving the existing application behavior.

### Verification

- Executed the behavior contract before and after the refactor.
- Performed manual API verification of status transitions and overdue filtering.
- Reran the complete pytest suite successfully.