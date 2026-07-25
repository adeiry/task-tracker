# Mid-Course Project Verification Report

This report records verification evidence for the corrected mid-course project implementation. All results, evidence, and PASS statuses must be based on actual test execution and manual verification.

## 1. Baseline Check

| Item | Value |
|---|---|
| Repository / commit | `mid-course-project` @ `3141b39` |
| Python version | Python 3.13.3 |
| Browser | Google Chrome 139.0.7258.154 |
| Backend URL | `http://127.0.0.1:8000` |
| Frontend entry point | `frontend/index.html` |
| Pytest version | pytest 9.1.1 |
| Test date | 2026-07-25 |

---

## 2. Backend Test Results

| Feature              | Verification                                              | Actual Result                                                                         | Status |
| -------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------ |
| Health endpoint      | `GET /health`                                             | Returned HTTP 200 with `status: "ok"` and a valid timestamp.                          | PASS   |
| Create task          | `POST /tasks` with a valid title                          | Task created successfully (HTTP 201) with a generated ID and expected default values. | PASS   |
| Update task          | `PATCH /tasks/{id}` with a partial payload                | Updated only the specified fields while preserving the remaining values.              | PASS   |
| Delete task          | `DELETE /tasks/{id}`, then `DELETE` again on a missing ID | Existing task returned HTTP 204. A second request returned HTTP 404.                  | PASS   |
| Status transitions   | Valid, invalid, and same-status `PATCH` transitions       | Valid transitions succeeded. Invalid and same-status transitions returned HTTP 422.   | PASS   |
| Status filtering     | `GET /tasks?status=`                                      | Returned only tasks matching the requested status.                                    | PASS   |
| Priority filtering   | `GET /tasks?priority=`                                    | Returned only tasks matching the requested priority.                                  | PASS   |
| Due dates            | Create, update, and clear `due_date`                      | Due dates were created, updated, and removed successfully.                            | PASS   |
| Overdue filtering    | `GET /tasks?overdue=true` and `overdue=false`             | Returned the correct overdue and non-overdue task sets.                               | PASS   |
| Tags                 | Create, update, normalize, and deduplicate tags           | Tags were stored correctly, normalized, and duplicate tags were removed.              | PASS   |
| Tag filtering        | `GET /tasks?tag=`                                         | Returned only tasks containing the requested tag.                                     | PASS   |
| Blank-tag validation | `POST`/`PATCH` with a blank or whitespace-only tag        | Invalid requests were rejected with HTTP 422.                                         | PASS   |

Run before recording results:

```bash
python -m pytest -v
```

---

## 3. Manual Browser Checks

| Behavior                        | Actual Result                                                                                                            | Status |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------ |
| Kanban columns                  | Three Kanban columns (To Do, In Progress, Done) were displayed correctly and tasks appeared in their respective columns. | PASS   |
| Loading state                   | Loading indicator was displayed while tasks were being fetched, then replaced by the Kanban board.                       | PASS   |
| Empty state                     | When no tasks existed, an empty-state message was displayed instead of an empty board.                                   | PASS   |
| Error state                     | An error message was displayed when the backend was unavailable or a request failed.                                     | PASS   |
| Drag and drop                   | Tasks could be dragged between valid columns, and status changes were persisted after the drop.                          | PASS   |
| Create task                     | A new task was created successfully through the UI and appeared immediately in the correct column.                       | PASS   |
| Edit task                       | Task details were updated successfully, and the changes were reflected immediately in the UI.                            | PASS   |
| Delete task                     | The selected task was removed successfully and no longer appeared on the board.                                          | PASS   |
| Due-date display                | Due dates were displayed correctly for tasks with assigned due dates.                                                    | PASS   |
| Overdue highlighting            | Tasks with overdue due dates were visually highlighted as overdue.                                                       | PASS   |
| Tag display                     | Task tags were displayed correctly and updated after editing.                                                            | PASS   |
| Frontend filters (overdue, tag) | Filtering by overdue status and tags displayed only the matching tasks.                                                  | PASS   |

---

## 4. Behavior Contract

### Before Refactor

The following behaviors were verified and recorded:

- Create task
- Edit task
- Delete task
- Status transitions
- Due dates
- Overdue filtering
- Tag filtering
- Blank-tag validation
- Drag and drop
- Loading / Empty / Error states

### After Refactor

The same verification checklist was executed after the refactor.

Result:

- No observable behavior changes.
- No regressions detected.
- All backend and frontend behaviors matched the pre-refactor baseline.

---

## 5. Break Test Evidence

Each Break Test follows the required Green → Red → Green workflow by:
1. Running the existing test successfully.
2. Introducing a temporary production-code change (without modifying the test).
3. Confirming the test fails.
4. Restoring the original code.
5. Confirming the test passes again.

### Break Test 1 — Blank-Tag Validation

**Protected behavior**

Blank or whitespace-only tags must be rejected with **HTTP 422** rather than being silently accepted.

**Test**

```bash
python -m pytest tests/test_tasks.py::test_create_task_blank_tag_among_valid_tags_returns_422 -v
```

| Step | Result |
|------|--------|
| Initial green run | **PASSED** (1 test passed). |
| Temporary production-code change | Modified `app/models.py` by replacing `raise ValueError("tags cannot be blank")` with `continue` in `_normalize_tags()`. |
| Red run | **FAILED** as expected. The API returned **HTTP 201 Created** instead of **HTTP 422**, confirming the test detected the introduced regression. |
| Source restoration | Restored the original `raise ValueError("tags cannot be blank")` statement in `app/models.py` and verified the change before rerunning the tests. |
| Final verification | The focused test passed again (**1 passed**), followed by a successful execution of the full test suite (**60 passed**). |

**Evidence**

- Initial green run (focused test)
- Expected failing test after introducing the defect
- Final green run (focused test)
- Full test suite passing (60 tests)

**Status:** **COMPLETED**

### Break Test 2 — Overdue Filtering

**Protected behavior**

A completed (`Done`) task with a past due date must **not** be treated as overdue.

**Test**

```bash
python -m pytest tests/test_tasks.py::test_list_tasks_overdue_true_excludes_done_task_with_past_due_date -v
```

| Step | Result |
|------|--------|
| Initial green run | **PASSED** (1 test passed). |
| Temporary production-code change | Modified `app/business_rules.py` by removing the `and task.status != TaskStatus.DONE` condition from `is_task_overdue()`. |
| Red run | **FAILED** as expected. A completed task with a past due date was incorrectly returned as overdue, confirming the test detected the introduced regression. |
| Source restoration | Restored the original `and task.status != TaskStatus.DONE` condition in `app/business_rules.py` and verified the change before rerunning the tests. |
| Final verification | The focused test passed again (**1 passed**), followed by a successful execution of the full test suite (**60 passed**). |

**Evidence**

- Initial green run (focused test)
- Expected failing test after introducing the defect
- Final green run (focused test)
- Full test suite passing (60 tests)

**Status:** **COMPLETED**

---

## Final Verification Summary

Before submission, confirm that:

- All backend verification checks have been completed.
- All manual browser checks have been completed.
- The behavior contract has been verified before and after the refactor.
- Both Break Tests have completed the Green → Red → Green workflow.
- Every PASS status is supported by real evidence.