# Mid-Course Project User Stories

## Feature 1: Due Dates

### US-01 — Add a due date

As a team member, I want to assign an optional due date to a task so that I know when the task should be completed.

#### Acceptance Criteria

- A task can be created without a due date.
- A task can be created with a valid due date.
- A task's due date can be updated.
- The due date is returned by the API.
- The due date is displayed on the task card.
- Invalid due-date values are rejected.

### US-02 — Identify overdue tasks

As a team member, I want overdue tasks to be clearly identified so that I can prioritize delayed work.

#### Acceptance Criteria

- A task is overdue when its due date is before the current date.
- Completed tasks are not treated as overdue.
- Overdue tasks have a visible indicator on the Kanban board.
- Tasks without a due date are not treated as overdue.

### US-03 — Filter overdue tasks

As a team member, I want to filter the board to show overdue tasks so that I can focus on tasks that need immediate attention.

#### Acceptance Criteria

- The frontend includes an overdue filter.
- Enabling the filter shows only overdue tasks.
- Disabling the filter restores the normal task list.
- The filter works together with the existing board states.

---

## Feature 2: Tags

### US-04 — Assign tags to a task

As a team member, I want to assign tags to a task so that I can categorize related work.

#### Acceptance Criteria

- A task can have zero or more tags.
- Tags can be added when creating a task.
- Tags can be changed when editing a task.
- Tags are returned by the API.
- Tags are displayed on the task card.

### US-05 — Validate tags

As a team member, I want tag values to be validated so that task data remains clear and consistent.

#### Acceptance Criteria

- Empty tag values are not stored.
- Duplicate tags are not stored more than once.
- Leading and trailing spaces are removed.
- Invalid tag input returns a validation error.

### US-06 — Filter tasks by tag

As a team member, I want to filter tasks by tag so that I can focus on a specific category of work.

#### Acceptance Criteria

- The frontend provides a tag filter.
- Selecting a tag shows only tasks containing that tag.
- Clearing the filter shows all tasks again.
- The tag filter works with the existing status and priority behavior.