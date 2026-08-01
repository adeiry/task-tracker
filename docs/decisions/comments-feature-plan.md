# Comments on Tasks — Feature Design Plan

Status: Proposed  
Scope: Design only; no implementation changes are included.

## 1. Data Model

The comment models should be added to `app/models.py`, alongside `TaskCreate`, `TaskUpdate`, and `TaskResponse`. The project currently keeps request and response models together rather than splitting them into separate packages.

Add two Pydantic models:

### `CommentCreate`

Client-supplied fields:

| Field | Type | Rules |
|---|---|---|
| `author` | `str` | Required; 1–100 characters |
| `body` | `str` | Required; 1–2000 characters |

Recommended conventions based on the existing task models:

- Set `extra="forbid"` so unknown request fields produce HTTP 422, matching `TaskCreate` and `TaskUpdate`.
- Reject blank and whitespace-only values.
- Do not accept `id`, `task_id`, or `created_at` from the client.
- Decide whether validation trims and stores both values or merely uses trimming to detect blank input. This is not determined by the existing code for comment bodies.

### `CommentResponse`

Server-produced fields:

| Field | Type | Source |
|---|---|---|
| `id` | `str` | Server-generated UUID4 string |
| `task_id` | `str` | Parent task ID taken from the route |
| `author` | `str` | Validated request value |
| `body` | `str` | Validated request value |
| `created_at` | `datetime` | Server-generated timezone-aware UTC datetime |

Use a UUID4 serialized as a string because `app/storage.py` generates task IDs with `str(uuid.uuid4())`. Generate `created_at` with `datetime.now(timezone.utc)`, matching task timestamp handling.

Do not add comments to `TaskResponse` initially. Keeping comments behind nested routes avoids changing the existing task response shape and prevents every task-list request from embedding comment collections.

No `CommentUpdate` model is proposed in the initial scope because editing comments was not requested. It can be added later if the team chooses to support editing.

## 2. API Routes

The existing application defines handlers directly in `app/main.py`, without an active router or service layer. For consistency, the initial comment handlers would also belong there. The packages under `app/api/`, `app/repositories/`, and `app/services/` are placeholders and should not be treated as implemented architecture.

### Create a comment

| Item | Design |
|---|---|
| Method | `POST` |
| Path | `/tasks/{task_id}/comments` |
| Request body | `CommentCreate`: `author`, `body` |
| Success | HTTP 201 |
| Response body | `CommentResponse` |
| OpenAPI tag | `comments` |

Processing:

1. Look up the parent with the existing `storage.get_task_by_id(task_id)` convention.
2. Return HTTP 404 if the task does not exist.
3. Generate the comment ID and UTC timestamp in the storage layer.
4. Derive `task_id` from the route; do not accept it in the request body.
5. Store and return the complete comment.

Reusing `storage.get_task_by_id(task_id)` preserves the route-to-storage interaction already used by `GET /tasks/{task_id}` and avoids introducing an unsupported service abstraction.

Error cases:

- HTTP 404 with a task-not-found detail when the parent task does not exist.
- HTTP 422 for a missing, blank, incorrectly typed, or over-length `author`.
- HTTP 422 for a missing, blank, incorrectly typed, or over-length `body`.
- HTTP 422 for unknown request fields, including client attempts to submit `id`, `task_id`, or `created_at`.

This follows the existing split between explicit route-level 404 responses and automatic Pydantic 422 responses.

### List comments for a task

| Item | Design |
|---|---|
| Method | `GET` |
| Path | `/tasks/{task_id}/comments` |
| Request body | None |
| Success | HTTP 200 |
| Response body | `list[CommentResponse]` |
| OpenAPI tag | `comments` |

Processing:

1. Verify that the parent task exists.
2. Return that task’s comments only.
3. Return an empty list when the task exists but has no comments.
4. Return comments in an explicitly documented order.

Recommended initial order: oldest first by `created_at`, with ID as a deterministic tie-breaker if necessary. Existing task-list ordering merely follows dictionary insertion order and is explicitly not documented as an intentional contract, so comment ordering should be decided rather than inherited accidentally.

Error case:

- HTTP 404 if the parent task does not exist.

### Routes not included initially

No single-comment retrieval, update, or deletion routes are included in this minimum design. If the team approves those operations later, nested paths such as `/tasks/{task_id}/comments/{comment_id}` would preserve the parent-child relationship. Their authorization, ownership, and mismatch behavior need decisions first.

## 3. Tests

API tests should be added to `tests/test_tasks.py` or, preferably for bounded organization, a new `tests/test_comments.py`. The repository currently uses function-based pytest tests, a shared `TestClient`, direct `client.get`/`client.post` calls, and descriptive names such as `test_create_task_valid_returns_201_with_full_body`.

`tests/conftest.py` automatically resets storage before and after every test and supplies `client` and `created_task` fixtures. The reset fixture must be extended to clear comment state as well, or `storage._reset()` must clear both stores.

### Happy path

- `test_create_comment_valid_returns_201_with_full_body`
- `test_create_comment_generates_uuid_string`
- `test_create_comment_sets_task_id_from_parent_route`
- `test_create_comment_sets_timezone_aware_utc_created_at`
- `test_list_comments_existing_task_returns_200`
- `test_list_comments_returns_only_comments_for_requested_task`
- `test_list_comments_existing_task_with_no_comments_returns_empty_list`
- `test_list_comments_returns_comments_in_documented_order`

The full-body assertion should verify exactly `id`, `task_id`, `author`, `body`, and `created_at`.

### Validation

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_whitespace_only_author_returns_422`
- `test_create_comment_author_one_character_returns_201`
- `test_create_comment_author_one_hundred_characters_returns_201`
- `test_create_comment_author_over_one_hundred_characters_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_whitespace_only_body_returns_422`
- `test_create_comment_body_one_character_returns_201`
- `test_create_comment_body_two_thousand_characters_returns_201`
- `test_create_comment_body_over_two_thousand_characters_returns_422`
- `test_create_comment_unknown_field_returns_422`
- `test_create_comment_rejects_client_supplied_server_fields`

If trimming is approved:

- `test_create_comment_trims_padded_author`
- `test_create_comment_handles_padded_body_according_to_documented_rule`

### Edge cases

- `test_create_comment_missing_task_returns_404_with_detail`
- `test_list_comments_missing_task_returns_404_with_detail`
- `test_comment_is_not_visible_under_different_task`
- `test_multiple_comments_receive_distinct_ids`
- `test_deleting_task_applies_documented_comment_policy`
- `test_storage_reset_clears_comments_between_tests`
- `test_comment_body_preserves_line_breaks`
- `test_comment_response_does_not_change_task_response_shape`

The existing manual `tests/verify_a.py` script checks selected Pydantic edge cases outside pytest. Comment model checks could be added there only if the team wants to preserve that secondary verification practice; automated API coverage should remain the primary verification.

## 4. Frontend Changes

The only confirmed frontend file is the self-contained `frontend/index.html`. It contains all HTML, CSS, and JavaScript and has no build step. Its API base URL is hardcoded to `http://localhost:8000`.

### Proposed user experience

Add a “Comments” action to each rendered task card beside the existing “Edit” action. Selecting it opens a task-comments view containing:

- The task title for context.
- A loading state while comments are fetched.
- An empty state such as “No comments yet.”
- A chronological comment list showing author, body, and formatted creation time.
- A form with required `author` and `body` fields.
- Client-side maximum lengths of 100 and 2000 characters.
- Submission, validation, and network error states.
- A disabled submit button while a comment is being created.

After a successful submission, append the returned comment or refetch the list and clear the body field. The author could remain populated for convenience, but persistence beyond the current page is an open product/privacy decision.

### Changes within `frontend/index.html`

The file would need updates to:

- Add CSS for the comments action, comments modal or panel, comment list, empty/loading states, and validation feedback.
- Add accessible comments markup, likely as a separate modal rather than mixing comment fields into the existing task create/edit form.
- Extend `renderTaskCard()` to render and bind a comments button.
- Add comment-view state separate from the existing `modalState`.
- Fetch `GET /tasks/{task_id}/comments` when the comments view opens.
- Submit `POST /tasks/{task_id}/comments`.
- Reuse `escapeHtml()` when rendering author and body to prevent user content from becoming executable markup.
- Reuse or generalize the existing server-error extraction behavior.
- Add keyboard, focus, close-button, overlay-click, and Escape-key handling consistent with the current task modal.

The existing task list response would remain unchanged, so `fetchTasks()` would not fetch comments for every board card. This avoids an additional request per task during initial board rendering.

No separate frontend test framework or automated browser-test configuration is visible. Frontend verification would therefore be manual unless the team separately approves and configures an automated approach.

## 5. Migration Notes

`app/storage.py` currently stores tasks in a module-level dictionary keyed by task ID. There is no database or durable migration mechanism.

For the current architecture:

- Add a separate in-memory comment store rather than embedding comments in `TaskResponse`.
- A store keyed by comment ID preserves direct identity, while a secondary task-to-comment index can support efficient listing. For this learning-project scale, filtering a comment dictionary by `task_id` is also possible but should be an explicit choice.
- Extend `storage._reset()` so it clears task and comment state.
- Existing tasks need no backfill because comments begin as an empty related collection.
- All comments will be lost on process restart, matching current task behavior.
- No database migration file or command is required under the confirmed architecture.
- No database migration tooling is visible, so a future persistent-storage migration is not confirmed.

Task deletion requires an explicit policy. The recommended policy for the current in-memory implementation is cascade deletion: deleting a task should remove all comments whose `task_id` matches it. That prevents orphaned comments and approximates a relational foreign key with `ON DELETE CASCADE`.

Changing `DELETE /tasks/{task_id}` to cascade internally would not alter its current HTTP 204 response. A regression test should prove that comments are removed.

## 6. Open Questions

1. **Task deletion policy:** Should deleting a task cascade-delete its comments, reject deletion while comments exist, or retain orphaned comments? Cascade deletion is the simplest fit for the current application.
2. **Comment mutability:** Are comments immutable after creation, or should authors be able to edit and delete them? Supporting either operation requires additional routes and product rules.
3. **Author identity:** The application has no authentication. Should `author` remain free-form input, or is a future authenticated identity expected to replace it?
4. **Whitespace behavior:** Should `author` and `body` be stored trimmed? For multiline bodies, trimming only outer whitespace while preserving internal spaces and line breaks may be preferable, but this is not specified.
5. **Ordering:** Should comments display oldest first for conversational reading or newest first for recency? This must be an explicit API contract.
6. **Frontend placement:** Should comments appear in a separate modal, inside the existing edit modal, or in a dedicated task-detail view? The current frontend has no dedicated task-details screen.
7. **Comment count:** Should task cards show a comment count? Doing so efficiently may require changing task-list responses, adding a count field, or making extra requests.
8. **Pagination:** Is an unpaginated comment list acceptable for this learning project, or should the API establish pagination now? No pagination convention is present in the existing task API.
9. **Rendering format:** Is the body plain text only, or should Markdown be supported? Plain text is safer and consistent with the current frontend’s escaped rendering.
10. **API scope:** Is create-and-list sufficient for the first increment, or must single-comment retrieval, editing, and deletion be included?

## Repository Grounding Verification

- The plan was based on `AGENTS.md`, `README.md`, the model, route, storage, and business-rule modules under `app/`, the pytest files under `tests/`, and `frontend/index.html`.
- It reuses confirmed conventions: Pydantic models in `app/models.py`, route handlers in `app/main.py`, UUID4 strings and timezone-aware UTC timestamps in `app/storage.py`, explicit route-level 404 responses, and automatic Pydantic 422 responses.
- The storage design preserves the existing module-level in-memory approach and explicitly notes restart data loss instead of assuming a database or migration framework.
- The test plan follows the repository’s function-based pytest naming, shared `TestClient`, `created_task` fixture, and autouse `storage._reset()` isolation pattern.
- The frontend proposal preserves the existing single-file vanilla JavaScript, modal, `fetch`, loading/error-state, and `escapeHtml()` patterns rather than inventing a framework or build step.
- The empty `app/api/`, `app/repositories/`, and `app/services/` packages are identified as placeholders, not treated as active layers or used to justify an architectural rewrite.
- Unsupported product choices—including deletion behavior, ordering, pagination, mutability, authentication, and whitespace handling—remain recommendations, assumptions, or open questions. This makes the design safer than a generic proposal because implementation work would follow confirmed repository constraints while surfacing decisions that still require human approval.

# Files read

- `AGENTS.md`
- `app/models.py`
- `app/main.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/conftest.py`
- `tests/test_tasks.py`
- `tests/verify_a.py`
- `frontend/index.html`
- `README.md`

# Assumptions to verify

- **Assumption:** The first increment needs only comment creation and listing.
- **Assumption:** Comments should remain separate from `TaskResponse`.
- **Assumption:** Comment IDs should follow the existing UUID4-string convention.
- **Assumption:** Unknown request fields should be forbidden, matching existing create/update models.
- **Assumption:** Blank and whitespace-only author and body values should be rejected.
- **Assumption:** Outer whitespace should be trimmed, while internal body whitespace and line breaks should be preserved.
- **Assumption:** Comments should be returned oldest first.
- **Assumption:** Deleting a task should cascade-delete its comments.
- **Assumption:** Comment bodies are plain text, not Markdown or HTML.
- **Assumption:** An unpaginated list is sufficient for the project’s current learning scope.
- **Assumption:** A separate comments modal is preferable to expanding the task-edit form.
- **Not confirmed:** Authentication, authorization, a persistent database, migration tooling, frontend automated tests, or a future task-detail screen.

## Generic vs Repo-Grounded Codex Comparison

**Biggest difference:** The generic plan described broadly applicable models, nested routes, tests, frontend states, and migration concerns, while the repo-grounded plan ties those ideas to this project’s actual Pydantic models, direct FastAPI handlers, module-level in-memory storage, pytest fixtures, and single-file vanilla JavaScript frontend.

**Plan I would hand to a teammate:** The repo-grounded plan, after the team resolves the documented open questions. It identifies the concrete files and existing helpers involved, preserves current project conventions, and separates confirmed repository facts from recommendations and assumptions.

**Where the generic plan was still useful:** It provided a sound feature checklist: separate request and response data, nested task-comment routes, validation boundaries, parent-not-found behavior, happy-path and edge-case tests, frontend loading and error states, deletion policy, ordering, and migration questions.

**Where repo grounding mattered most:** It established that storage is an in-memory dictionary rather than a database, routes live directly in `app/main.py`, placeholder packages are not implemented architecture, tests depend on the autouse reset fixture, and all frontend changes belong in `frontend/index.html` with no confirmed build or automated browser-test setup.
