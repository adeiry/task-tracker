# Task Tracker Architecture

## 1. What the app does

The Task Tracker is a FastAPI REST API that supports health checks and creating, listing, retrieving, partially updating, and deleting tasks. Task lists can be filtered by status, priority, overdue state, and tag.

## 2. Data model

The primary entity is `Task`, represented through three Pydantic models:

- `TaskCreate`: title, description, status, priority, assignee, due date, and tags.
- `TaskUpdate`: optional versions of the editable fields for partial updates.
- `TaskResponse`: the complete task, adding a string ID plus creation and update timestamps.

Statuses are `ToDo`, `InProgress`, and `Done`. Priorities are `Low`, `Medium`, and `High`. New tasks default to `ToDo` and `Medium`; optional values include assignee and due date.

## 3. Request flow

When a client sends `POST /tasks`, FastAPI parses the body as `TaskCreate`. Pydantic rejects unknown fields and validates the title and tags. The route passes the validated model to `storage.add_task`, which generates a UUID4 string and a UTC timestamp, constructs a `TaskResponse`, stores it in the module-level `_tasks` dictionary, and returns it. FastAPI serializes the task as the response with HTTP 201.

## 4. Key files

- `app/main.py` — Creates the FastAPI app, configures CORS, and defines health and task CRUD routes.
- `app/models.py` — Defines task request/response models, enums, defaults, and field validation.
- `app/storage.py` — Implements in-memory task creation, lookup, filtering, updating, and deletion.
- `app/business_rules.py` — Referenced for status-transition, overdue, and tag-matching logic; its implementation is **not visible from the files I read**.
- Frontend entry file — **not visible from the files I read**.
- Dependency/configuration files — **not visible from the files I read**.

## 5. Conventions

- **Validation:** Pydantic models reject unknown fields. Titles are trimmed, must be nonblank, and may contain at most 200 characters. Tags are trimmed, reject blank entries, and are deduplicated case-insensitively while preserving the first casing.
- **Storage:** Tasks are held in a module-level dictionary keyed by generated UUID4 strings. Creation and nonempty updates use UTC timestamps. Persistence beyond the running process is **not visible from the files I read**.
- **Error handling:** Missing task IDs produce HTTP 404 responses. Request-model failures produce FastAPI/Pydantic HTTP 422 responses. Invalid status transitions are delegated to a business-rule function whose implementation is **not visible from the files I read**.
- **Updates:** PATCH applies only explicitly supplied fields. An empty update leaves the task and timestamp unchanged; an explicit null remains part of the update.
- **Frontend/backend interaction:** **not visible from the files I read**.
- **CORS:** The API permits all origins, methods, and headers and enables credentials.

## 6. Not visible or assumptions

Authentication, authorization, database use, durable persistence, deployment, dependency versions, frontend implementation, frontend API configuration, automated tests, API startup commands, status-transition rules, overdue calculation details, tag-filtering details, and production topology are **not visible from the files I read**. No assumptions about them are made here.
